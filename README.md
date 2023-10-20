# Part 4 Project: Auto-complete for Music
This is a final year engineering research project, specialising in machine learning/AI and embedded systems. 

🏆*Category winner for Embedded Systems - 1* awarded by industry judges from Invenco.

Recent music generation models have become increasingly complex to generate realistic-sounding music. Over 63% of the models we reviewed had over 40 million parameters. While the music generated from these 
models is almost realistic to a human composition, the models require high computational resources, such as a computer with multiple GPUs. This makes it inaccessible to composers who are financially struggling or 
in developing nations. Even if these models are hosted online through in-cloud executions, composers who don't have reliable internet connections won't be able to use them.

## Research Question
Can we get adequate music generation while lowering the computational requirement to produce and run the model?

## Research Contributions
- A lightweight model that can be used on edge devices such as Raspberry Pi or mobile phones.
- A relatively fast generation time without using a GPU or cloud-based execution.
- Ideally to generate music that is almost comparable to existing models.
- Limited to the classical genre due to the wide variety of datasets available and the well-structured nature of those compositions.



## Contributors
- Rachel Nataatmadja
- Shou Miyamoto

## Interactive Demonstration 
You can run the model on your computer. We have given 5 preprocessed prompts for you to choose from in the demonstration. It will generate a continuation of the musical prompt you give in.

### How to run
The interactive demonstration is under the `pyqt_demo_code` folder. In that folder, please read the README.md for project setup. Once you have installed the required packages and set up FluidSynth, here is some instructions on how to run:
1. Change your directory to the `pyqt_demo_code` folder using `cd pyqt_demo_code`
2. Run the `music_gen_demo.py` file using the run button or type `python music_gen_demo.py` in command line.

Note: that the files generated (i.e. wav and midi files) are located in `pyqt_demo_code/music_python/outputs` folder.
