.. _intro-chapter:

#############
Introduction
#############

***************************
Purpose and Target Audience
***************************

First and foremost, a couple important terms:

**Software-Defined Radio (SDR):**
    A radio that uses software to perform signal-processing tasks that were traditionally performed by hardware
  
**Digital Signal Processing (DSP):**
    The digital processing of signals, in our case RF signals
  
This textbook is designed for someone who is:

#. Interested in *using* SDRs to do cool stuff
#. Good with Python
#. Relatively new to DSP, wireless communications, and SDR
#. A visual learner, preferring animations over equations
#. Better at understanding equations *after* learning the concepts
#. Looking for concise explanations, not a 1,000 page textbook

A perfect candidate might be an advanced Computer Science student interested in a job involving wireless communications after graduation.  Those who have little Python experience yet a solid foundation in MATLAB, Ruby, or Perl may be fine after familiarizing themselves with Python's syntax.

This textbook is meant to introduce concepts quickly and smoothly, enabling the reader to perform DSP and use SDRs intelligently.  It's not meant to be a reference textbook for all DSP/SDR topics; there are plenty of great textbooks already out there, such as `Analog Device's SDR textbook
<https://www.analog.com/en/education/education-library/software-defined-radio-for-engineers.html>`_ and `dspguide.com <http://www.dspguide.com/>`_.  You can always use Google to recall trig identities or Shannon's limit.  Think of this textbook like a gateway into the world of DSP and SDR: it's lighter and less of a time and monetary commitment, when compared to more traditional courses and textbooks.

This textbook was designed specifically for students in Computer Science, although it can be used by anyone itching to learn about SDR who has programming experience.  As such, it covers the necessary theory to understand DSP techniques without the intense math that is usually included in DSP courses.  Instead of burying ourselves in equations, an abundance of images and animations are used to help convey the concepts.  I believe that equations are best understood *after* learning the concepts through visuals and practical exercises.

To cover foundational DSP theory, an entire semester of "Signals and Systems", a typical course within electrical engineering, is condensed into a few chapters.  Once the DSP fundamentals are covered, we lauch into SDRs, although DSP and wireless communications concepts continue to come up throughout the textbook.

Code examples are provided in Python.  They utilize NumPy, which is Python's standard library for arrays and high-level math.  The examples also rely upon Matplotlib, which is a Python plotting library that provides an easy way to visualize signals, arrays, and complex numbers.  Note that while Python is "slower" than C++ in general, many math functions within Python/NumPy are implemented in C/C++ and heavily optimized; the SDR API is simply a set of Python bindings for C/C++ functions/classes.


***************
Contributing
***************

If you get through any amount of this textbook and email me at pysdr@vt.edu with questions/comments/suggestions, then congratulations, you will have contributed to this textbook!

But on a more grand scale, you can help contribute to this textbook in the same way as any open source software project- through Git.  This textbook might be in the form of a website, but the source material it's generated from all lives on the `textbook's GitHub page <https://github.com/777arc/textbook>`_.  Feel free to submit an issue or even a Pull Request (PR) with fixes or improvements.  Those who submit valuable feedback/fixes will be permanently added to the acknowledgments section below.  Not good at Git but have changes to suggest?  Feel free to email me at pysdr@vt.edu.

The website this textbook is hosted on is ad-free because we all hate ads.  I also don't provide a PayPal or Bitcoin address where I accept donations.  There is literally no way for me to get paid for this textbook.  Instead, I merely suggest sharing this textbook with colleagues, students, and other lifelong learners who may be interested in the material.

*****************
Acknowledgements
*****************

Thank you to anyone who has read any portion of this textbook and provided feedback, and especially to:

- `Barry Duggan <http://github.com/duggabe>`_
- Matthew Hannon
- James Hayek
- `Deidre Stuffer <http://kd9qgl.wordpress.com/>`_
