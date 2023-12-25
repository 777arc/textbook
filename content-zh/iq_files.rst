.. _iq-files-chapter:

##################
IQ 文件以及 SigMF
##################

在前文的所有 Python 示例中，我们将信号存储为了类型为“complex float”的一维 NumPy 数组。
在这一章中，我们将学习如何将信号存储到文件以及如何读入到 Python 里，同时介绍 SigMF 标准。
将信号数据存储在文件中是非常有用的：有时你需要对信号做离线分析、与同事分享、或者打包成数据集。

*************************
二进制文件
*************************

我们还记得，数字基带信号其实是就是一串复数。

比如： [0.123 + j0.512, 0.0312 + j0.4123, 0.1423 + j0.06512, ...]

以上数据对应 [I+jQ, I+jQ, I+jQ, I+jQ, I+jQ, I+jQ, I+jQ, ...]

当我们要将复数保存到文件中时，我们会使用IQIQIQIQIQIQIQIQ这样的格式进行保存。
也就是说，我们按顺序存储了一系列浮点数。在读取它们时，我们必须将其重新分离成[I+jQ, I+jQ, ...]的形式。

虽然我们可以将这一长串复数存储在文本文件或CSV文件中，但我们更倾向于将它们保存在所谓的“二进制文件”中以节省空间。
毕竟在高采样率下，你所记录的信号文件可能轻松超过多个 GB。
如果你直接在文本编辑器中打开一个二进制文件，它看起来可能和下面的截图差不多。
二进制文件包含了一系列字节，所以你必须自己按照约定的格式解析，但是二进制文件通常是存储数据最高效的方式（同时还有各种压缩算法可用）。
由于我们的信号通常是随机序列般的一串浮点数，所以我们通常不会对其进行压缩。当然，二进制文件也被用于许多其他事情，例如编译过的程序（binaries）。
用于保存信号时，我们称它们为二进制的“IQ 文件”，使用文件扩展名 .iq。

.. image:: ../_images/binary_file.png
   :scale: 70 %
   :align: center

在 Python 中，默认的复数类型是 np.complex128，它使用两个 64 位浮点数 （float64）来表示一个复数。
但是在 DSP/SDR 领域，我们倾向于使用32位的浮点数（float32），
毕竟我们的 SDR 设备上的 ADC 硬件并不能提供高达 float64 的精度。
因此在 Python 代码中，我们实际使用的是 **np.complex64** ，即用两个 float32 来表示一个复数。
其实在写代码时，复数到底是哪种类型并不重要。重要的是当你把数据保存到文件时，请确保它是以 np.complex64 类型的数组存储的。

*************************
Python 代码示例
*************************

在 Python 中，我们使用 :code:`tofile()` 函数将 NumPy 数组存储到文件中。
以下是创建一个简单 BPSK（二进制相位偏移键控）信号加噪声并将其保存到同一目录下的文件的代码：

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt

    num_symbols = 10000

    x_symbols = np.random.randint(0, 2, num_symbols)*2-1 # 由 -1 或者 1 组成的随机序列
    n = (np.random.randn(num_symbols) + 1j*np.random.randn(num_symbols))/np.sqrt(2) # AWGN (加性白高斯噪声) with unity power
    r = x_symbols + n * np.sqrt(0.01) # 0.01 功率的噪声
    print(r)
    plt.plot(np.real(r), np.imag(r), '.')
    plt.grid(True)
    plt.show()

    # 将数据保存到 IQ 文件中
    print(type(r[0])) # 检查数据类型，应该是 np.complex128!
    r = r.astype(np.complex64) # 转换为 np.complex64 类型
    print(type(r[0])) # 确认一下类型是否转换成功
    r.tofile('bpsk_in_noise.iq') # 保存到文件中

可以看看生成的文件包含多少字节。
理论上应该是 num_symbols * 8 ，因为我们使用的是 np.complex64 类型，每个采样点 8 字节（由 2 个 float32 构成，每个长 4 字节）。

我们可以使用 :code:`np.fromfile()` 来读取这个文件，代码如下：

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt

    samples = np.fromfile('bpsk_in_noise.iq', np.complex64) # 读取文件，记得传入数据类型
    print(samples)

    # 绘制 IQ 图
    plt.plot(np.real(samples), np.imag(samples), '.')
    plt.grid(True)
    plt.show()

一个常见的错误是忘记给 :code:`np.fromfile()` 传入文件的数据类型。
由于二进制文件不包含格式信息，默认情况下，:code:`np.fromfile()` 会认为它读入的是一个 float64  数组。

其他编程语言也都有各自读取二进制文件的方法，例如在MATLAB中，你可以使用 :code:`fread()` 函数。
若你想对文件进行可视化分析，请阅读后文内容。

如果你需要处理的数据类型是 int16（也就是短整型）或任何其他 NumPy 并不能映射成复数的类型，那么即使它们真实意义是复数，
你也只能先以实数类型读取，然后将它们交错重组回 IQIQIQ... 形式，下面展示了两种不同的方法：

.. code-block:: python

 samples = np.fromfile('iq_samples_as_int16.iq', np.int16).astype(np.float32).view(np.complex64)

或者

.. code-block:: python

 samples = np.fromfile('iq_samples_as_int16.iq', np.int16)
 samples /= 32768 # 转换到 -1 至 + 1 之间 (此步骤可选)
 samples = samples[::2] + 1j*samples[1::2] # 转换为 IQIQIQ... 格式

*********************************
可视化分析 IQ 文件 (RF 记录)
*********************************

虽然我们在 :ref:`freq-domain-chapter` 章节学习了如何用代码绘制时频谱（瀑布图），但那肯定不如直接用现成的软件快捷简单。
如果你需要分析 RF 记录（IQ 文件）且不想安装任何软件，那么推荐你使用 `IQEngine <https://iqengine.org>`_ 网站，它是一个用于分析、处理和共享 RF 记录的完整工具包。

如果你想安装专门的应用程序，可以使用 `inspectrum <https://github.com/miek/inspectrum>`_ 。inspectrum 是一个相当简单但功能强大的 RF 可视化工具，可以调节色彩映射范围和FFT窗口大小。你可以按住 Alt 键并使用滚轮来在时间轴上进行移动。还可以用内置的测量光标来定位信号之间的时间差，它还支持导出 RF 中的片段到新文件。对于 Ubuntu/Debian 系统，你可以安装如下：

.. code-block:: bash

 sudo apt-get install qt5-default libfftw3-dev cmake pkg-config libliquid-dev
 git clone https://github.com/miek/inspectrum.git
 cd inspectrum
 mkdir build
 cd build
 cmake ..
 make
 sudo make install
 inspectrum

.. image:: ../_images/inspectrum.jpg
   :scale: 30 %
   :align: center

*************************
最大值与饱和
*************************

当从 SDR 设备接收样本数据时，你必须了解样本数据的最大值。
许多 SDR 设备默认最大值为 1.0，最小值为 -1.0，以浮点数类型输出。
还有一些 SDR 设备会以整数形式提供样本（通常是 int16），在这种情况下，最大和最小值分别会是 +32767 和 -32768（除非另有说明），
你可以选择除以 32,768 将其转换为 -1.0 到 1.0 之间的浮点数。
了解你的 SDR 输出的最大值非常重要，这样才能知道如何检查“饱和错误”：当接收到一个极端响亮的信号（或者接收增益设置得太高）时，接收器将会“饱和”，
同时将超越饱和值的样本点全部截断（毕竟 ADC 的硬件位数是有限的）。在开发 SDR 应用时，请时刻警惕过饱和的问题。

一个过饱和的信号在时域内看起来就像锯齿一样不平滑：

.. image:: ../_images/saturated_time.png
   :scale: 30 %
   :align: center
   :alt: Example of a saturated receiver where the signal is clipped

过饱和导致的截断会在时域上制造突变，这会让频域看起来很糊。换句话说，频域会包含由于截断而引入的错误特征，这些特征并不属于真实信号，并且可能会在我们后续分析信号时导致误解。

*****************************
SigMF 以及如何标注 IQ文件
*****************************

因为 IQ 文件本身并不包含任何元数据（metadata），所以常见的做法是顺便创建第二个文件（文件名相同但文件扩展名是 .txt 或其他类型），
让这个文件记录信号的相关信息，至少要包括收集信号的采样率，以及 SDR 设备的接收中心频率。
在分析信号之后，元数据文件还可以包含针对有趣特征采样点的索引范围，例如能量峰值点所在的位置。
索引是一个从 0 递增的整数，唯一对应到一个位置上递增的采样点（即一个复数）。
比如，假设你知道从第 492342 个样本点到第 528492 个样本点之间有能量，
那么你可以读取文件后直接提取对应数组：:code:`samples[492342:528493]`。

幸运的是，目前已经有了针对信号记录的元数据格式的开放标准，称为 `SigMF <https://github.com/gnuradio/SigMF>`_ 。
通过使用 SigMF 这样的开放标准，多方可以更轻松地共享 RF 记录，并使用不同的工具来操作相同的数据集，例如 `IQEngine <https://iqengine.org/sigmf>`_ 。
它还可以防止 RF 数据集的“位腐烂”（bitrot）：随着时间的推移，由于一些细节没有与记录本身放在一起，
这些细节就因为遗忘而丢失掉了，只能重新花力气和时间分析。

使用 SigMF 描述你的 IQ 文件的最简单的方式是：将 .iq 文件重命名为 .sigmf-data，
创建一个新文件，该文件具有相同的名称但扩展名为 .sigmf-meta，
确保这个元数据文件中的 datatype 字段与数据文件的二进制格式匹配。这个元文件是一个 json 格式的纯文本文件，
你可直接用文本编辑器打开它并手动填写（稍后我们将讨论如何以编程方式进行此操作）。这里有一个 .sigmf-meta 文件的例子，你可以用它作为模板：

.. code-block::

 {
     "global": {
         "core:datatype": "cf32_le",
         "core:sample_rate": 1000000,
         "core:hw": "PlutoSDR with 915 MHz whip antenna",
         "core:author": "Art Vandelay",
         "core:version": "1.0.0"
     },
     "captures": [
         {
             "core:sample_start": 0,
             "core:frequency": 915000000
         }
     ],
     "annotations": []
 }

注意到 :code:`core:cf32_le` 表示你的 .sigmf-data 文件是 32 位浮点数记录的 IQIQIQIQ... 数据，
即上文所说的 np.complex64 复数采样点。有关其他可用数据类型，请参考 SigMF 官方文档（例如你的数据是实数类型而不是复数类型，或者你使用的是 16 位整数而不是浮点数来节省空间）。

除了数据类型，最重要的元数据项是：:code:`core:sample_rate` 和 :code:`core:frequency` 。
最好也记录采集设备的硬件信息（:code:`core:hw`），这包括 SDR 设备类型和天线信息。
你还可以在 :code:`core:description` 中记录其他描述信息。
:code:`core:version` 则表示创建元数据文件时所使用的 SigMF 标准的版本。

如果你喜欢用 Python 脚本来直接收集 RF 信号（比如一些 SDR 框架的 Python API），
那么你可以借助 SigMF Python 包来简化上文的步骤。
在 Ubuntu/Debian 系统上，你可以按照以下步骤安装：

.. code-block:: bash

 cd ~
 git clone https://github.com/gnuradio/SigMF.git
 cd SigMF
 sudo pip install .

借助这个包，为本章开头部分的例子编写 .sigmf-meta 文件的 Python 代码如下，我们在此例子中保存了 bpsk_in_noise.iq 文件：

.. code-block:: python

 import numpy as np
 import datetime as dt
 from sigmf import SigMFFile

 # <来源于上文示例代码>

 # r.tofile('bpsk_in_noise.iq')
 r.tofile('bpsk_in_noise.sigmf-data') # 将上面一行替换为次行

 # 创建元数据
 meta = SigMFFile(
     data_file='example.sigmf-data', # 这个后缀可以自定义
     global_info = {
         SigMFFile.DATATYPE_KEY: 'cf32_le',
         SigMFFile.SAMPLE_RATE_KEY: 8000000,
         SigMFFile.AUTHOR_KEY: 'Your name and/or email',
         SigMFFile.DESCRIPTION_KEY: 'Simulation of BPSK with noise',
         SigMFFile.VERSION_KEY: sigmf.__version__,
     }
 )

 # 在索引 0 号位记录一个标记信息
 meta.add_capture(0, metadata={
     SigMFFile.FREQUENCY_KEY: 915000000,
     SigMFFile.DATETIME_KEY: dt.datetime.utcnow().isoformat()+'Z',
 })

 # 检查错误后保存文件
 meta.validate()
 meta.tofile('bpsk_in_noise.sigmf-meta') # 这个后缀可以自定义

你仅需将上面代码中的 :code:`8000000` 和 :code:`915000000` 分别替换为你所使用的采样率和中心频率。

要在 Python 中读取 SigMF 文件请使用以下代码。
在这个例子中，两个 SigMF 文件命名为：:code:`bpsk_in_noise.sigmf-meta` 和 :code:`bpsk_in_noise.sigmf-data`。

.. code-block:: python

 from sigmf import SigMFFile, sigmffile

 # 载入数据集
 filename = 'bpsk_in_noise'
 signal = sigmffile.fromfile(filename)
 samples = signal.read_samples().view(np.complex64).flatten()
 print(samples[0:10]) # 让我们看看前十个采样点

 # 获取所需元数据
 sample_rate = signal.get_global_field(SigMFFile.SAMPLE_RATE_KEY)
 sample_count = signal.sample_count
 signal_duration = sample_count / sample_rate

更多细节请参考 `SigMF 官方文档 <https://github.com/gnuradio/SigMF>`_.

谢谢你阅读到这，给你一个小彩蛋：SigMF 的 Logo 实际上是以 SigMF 文件存储的，当该信号的星座图（IQ图）随时间变化时，它将产生以下动画：

.. image:: ../_images/sigmf_logo.gif
   :scale: 100 %
   :align: center
   :alt: The SigMF logo animation

如果你好奇的话，可以自己试试用下面这段 Python 代码读取它们的 `Logo 文件  <https://github.com/gnuradio/SigMF/tree/master/logo>`_ 并生成以上的动画。

.. code-block:: python

 import numpy as np
 import matplotlib.pyplot as plt
 import imageio
 from sigmf import SigMFFile, sigmffile

 # 装载数据集
 filename = 'sigmf_logo' # 假设这个文件和此脚本在同一目录下
 signal = sigmffile.fromfile(filename)
 samples = signal.read_samples().view(np.complex64).flatten()

 # 在尾部补零，这样动画循环时会容易看出来
 samples = np.concatenate((samples, np.zeros(50000)))

 sample_count = len(samples)
 samples_per_frame = 5000
 num_frames = int(sample_count/samples_per_frame)
 filenames = []
 for i in range(num_frames):
     print("frame", i, "out of", num_frames)
     # 生成每一帧
     fig, ax = plt.subplots(figsize=(5, 5))
     samples_frame = samples[i*samples_per_frame:(i+1)*samples_per_frame]
     ax.plot(np.real(samples_frame), np.imag(samples_frame), color="cyan", marker=".", linestyle="None", markersize=1)
     ax.axis([-0.35,0.35,-0.35,0.35]) # 固定坐标轴和坐标点
     ax.set_facecolor('black') # 背景颜色

     # 将帧保存到文件中
     filename = '/tmp/sigmf_logo_' + str(i) + '.png'
     fig.savefig(filename, bbox_inches='tight')
     filenames.append(filename)

 # 创建 gif 图
 images = []
 for filename in filenames:
     images.append(imageio.imread(filename))
 imageio.mimsave('/tmp/sigmf_logo.gif', images, fps=20)



