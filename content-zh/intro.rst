.. _intro-chapter:

#############
简介
#############

***************************
目标及受众
***************************

首先，需要介绍几个重要术语：

**软件定义无线电（SDR，Software-Defined Radio）：**
    一种无线电，利用软件来执行传统上由硬件执行的信号处理任务。
  
**数字信号处理（DSP， Digital Signal Processing）：**
    数字信号处理，就我们的案例而言是指射频（RF）信号的处理。

这本教科书是对DSP、SDR和无线通信领域的实践性入门。它适合以下人士：

#. 对 *使用* SDR做酷炫事物感兴趣的人
#. 擅长Python编程的人
#. 对DSP、无线通信和SDR相对比较新手的人
#. 是一个视觉学习者，偏好动画而非公式
#. 在学习概念 *之后* 更容易理解公式的人
#. 寻找简洁解释而不想要一本1,000页的教科书的人

举个例子，如果你是一名计算机科学专业的学生，对毕业后从事无线通信的工作感兴趣，那么这本书就非常适合你！当然，任何渴望学习SDR并且有编程经验的人也都适合看这本教材。为达到这个目的，这本书涵盖了理解DSP技术所需的必要理论，而不包括传统DSP课程中的复杂数学内容。我们不会沉浸在方程式中，而是使用大量的图像和动画来帮助传达概念，比如，你可以看看下图中傅里叶级数在复平面上制造的动画。我认为，在通过视觉和实践练习学习概念 *之后* ，数学公式才能被更好地理解。正是因为大量使用了动画，所以PySDR永远不会有在亚马逊上出售的纸质版本。

.. image:: ../_images/fft_logo_wide.gif
   :scale: 70 %   
   :align: center

本教科书旨在快速、流畅地介绍概念，使读者能够智慧地利用DSP和SDR。它不是旨在成为所有DSP/SDR主题的参考教科书；毕竟，已经有很多优秀的教科书了，比如 `Analog Device出版的SDR教材
<https://www.analog.com/en/education/education-library/software-defined-radio-for-engineers.html>`_ 和 `dspguide.com <http://www.dspguide.com/>`_ 这个网站。同时，你总是可以使用Google来回忆三角恒等式或香农极限。你可以把这本教科书看作是进入DSP和SDR世界的入口：与更传统的课程和教科书相比，它更轻便，需要投入的时间和金钱也更少。

为了涵盖基础的DSP理论，电子工程专业中一个典型的课程《信号与系统》在这本书中被压缩成了几个章节。一旦DSP基础部分讲解结束，我们就会转向SDR的内容，但是，DSP和无线通信的概念仍然会不断出现，贯穿整本教材。

示例代码使用Python编写。它们利用了NumPy，这是Python的标准库，用于数组操作和高级数学计算。这些示例还依赖于Matplotlib，这是一个Python绘图库，它提供了一种简单的方法来可视化信号、数组和复数。注意，虽然Python通常比C++“慢”，但Python/NumPy中的大多数数学功能是用C/C++实现并且进行了大量优化的。同样，我们使用的SDR API只是一组为C/C++函数/类编写的Python绑定。对于那些Python经验不多但在MATLAB、Ruby或Perl上有扎实基础的人来说，在熟悉Python的语法后应该不会遇到困难。


***************
贡献
***************

如果你从PySDR中受益，请与你的同事、学生以及其他可能对这些材料感兴趣的终身学习者分享。你也可以通过PySDR的 `Patreon <https://www.patreon.com/PySDR>`_ 捐款来表示支持，你的名字将会出现在每一页的章节列表下方的左侧。

如果你阅读了这本教科书的任何部分，并且通过 pysdr@vt.edu 给我发送了问题/评论/建议的电子邮件，那么恭喜你将为这本教科书做出贡献！你也可以直接在教科书的 `GitHub页面 <https://github.com/777arc/textbook/tree/master/content>`_ 编辑源代码（请创建一个新的Pull Request）。欢迎提交Issue或含有修复或改进的Pull Request（PR）。那些提交有价值的反馈/修复的人将被永久添加到下文的鸣谢部分。不擅长使用Git但有修改建议？随时通过 pysdr@vt.edu 联系我。

*****************
鸣谢
*****************

谢谢所有阅读过这本教科书任何部分并提供反馈的人，特别感谢以下人员：

- `Barry Duggan <http://github.com/duggabe>`_
- Matthew Hannon
- James Hayek
- Deidre Stuffer
- Tarik Benaddi 将PySDR翻译为 `法语 <https://pysdr.org/fr/index-fr.html>`_
- `Daniel Versluis <https://versd.bitbucket.io/content/about.html>`_ 将PySDR翻译为 `荷兰语 <https://pysdr.org/nl/index-nl.html>`_
- `mrbloom <https://github.com/mrbloom>`_  将PySDR翻译为 `乌克兰语 <https://pysdr.org/ukraine/index-ukraine.html>`_

以及所有 `PySDR Patreon <https://www.patreon.com/PySDR>`_ 支持者!
