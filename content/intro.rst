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
#. Looking for concise explanations, not a 1000 page textbook

A perfect candidate might be a student towards the end of a Computer Science degree, interested in getting a job involving wireless communications after graduation.  If you don't have much Python experience but are an expert with MATLAB, Ruby, or Perl, then you will probably be fine after spending a little time getting a feel for Python's syntax.

This textbook is meant to propel a student as quickly and smoothly as possible through many difficult concepts, enabling the student to perform DSP and use SDRs intelligently.  It's not meant to be a reference textbook for all DSP/SDR topics; there are plenty of great textbooks already out there, such as `Analog Device's SDR textbook 
<https://www.analog.com/en/education/education-library/software-defined-radio-for-engineers.html>`_ and `dspguide.com <http://www.dspguide.com/>`_.  You can always use Google to recall trig identities or Shannon's limit.  Think of this textbook like a gateway into the world of DSP and SDR; it's lighter and less of a time and monetary commitment, when compared to more traditional courses and textbooks.

This textbook was designed specifically for students in Computer Science, although it can be used by anyone itching to learn about SDR who has programming experience.  As such, it covers the necessary theory to understand DSP techniques, without the intense math that is usually included in DSP courses.  Instead of burying ourselves in equations, an abundance of images and animations are used, to help convey the concepts.  I believe that equations are best understood *after* learning the concepts through visuals and practical exercises.

In order to cover the foundational theory, an entire semester of "Signals and Systems", a typical course within electrical engineering, is condensed down into a few chapters.  Once the basic DSP fundamentals are covered, we jump into using software-defined radios (SDRs), although DSP and wireless communications concepts continue to come up throughout the textbook.

Coding examples are provided in Python.  We use NumPy, which is Python's standard library for arrays and high-level math, and comes with most Python installs.  We also use Matplotlib, which is a Python plotting library that provides an easy way for us to visualize signals, arrays, and complex numbers.  Note that while Python is "slower" than C++ in general, almost all of the math functions we will be using are implemented in C/C++ and heavily optimized, and the SDR API we will use is simply a set of Python bindings for C++ functions/classes.


***************
Contributing
***************

If you get through any amount of this textbook and email me at pysdr@vt.edu with questions/comments/suggestions, then congratulations, you will have contributed to this textbook!

But on a more grand scale, you can help contribute to this textbook in the same way as any open source software project- through git.  This textbook might be in the form of a website, but the source material it's generated from all lives on the `textbook's GitHub page <https://github.com/777arc/textbook>`_.  Feel free to submit an issue, or even a Pull Request (PR) with fixes or improvements.  Those who submit valuable feedback/fixes be permanently added to the acknowledgments section below.  Not good at Git but have changes to suggest?  Feel free to email me at pysdr@vt.edu.

The website this textbook is hosted on is ad-free, because we all hate ads.  I also don't provide a paypal or bitcoin address where I accept donations.  There is literally no way for me to get paid for this textbook.  Instead, I merely suggest just trying to share this textbook with colleagues who may be interested in the material. 

*****************
Acknowledgements
*****************

Thank you to anyone who has read any portion of this textbook and provided feedback, and especially to:

- Barry Duggan, KV4FV
- Matthew Hannon

