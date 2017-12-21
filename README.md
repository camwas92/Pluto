# Pluto: Take your Finances out of this Solar System #
This code is used for an postgraduate thesis, it focuses on understanding the potential of 
Reinforcement Learning to optimise a stock portfolio given current and project prices

##### Metadata #####
**Author:** Cameron Wasilewsky

**University:** University of Sydney

**Profession:** Consultant

**Build Dates:** 10 Nov 2017 to Ongoing
## Instructions ##

To run the code an individual will need a video file of the splashes. This will need to be put in a
folder called input which is in the same directory as this code. The user should then run 'dugong.py',
making the appropriate choices when needed

## Purpose ##

## Code Structure ##
* **Base Folder:**
    * (1) dugong.py - _Main function run on the code to identify all objects and admin functions_
    * **CoreFunctions:**
        * (2) LabelVideo.py - _Saving and labeling splashes, can be manual, watching the video or automatic from csv file_
        * (3) FileManipulation.py - _Code is used to structure images within directories to allow for easy training and transformations_
        * (4) Process.py - _This function runs the video with splash identification identified on the image, all frames shown are marked up_
        * (5) Training.py - _This function calls all training requirements. This includes but is not limited to the machine learning
        techniques used to classify frames with splashes, as well as the splash identification deep learning models._
        * (6) VideoBreakdown.py - _Call the pretrained model to breakdown an entire video classifing frames into
        splash or no splash, they are then aggregated and times of interest are identified._
    * **Identify:**
        * (7) Horizon.py - _Defines both the horizon and AOI class. There are also functions to extract the core data for these element_
        * (8) Splash.py - _Defines the splash class. There are also functions to extract the core data for this element_
        * (9) Target.py - _Defines the target class. There are also functions to extract the core data for this element_
        * **ImageProcessing:**
            * (10) ImageTransform.py - _Any transforms required such as Canny, Laplace or AOI extraction_
    * **Model:**
        * (11) Classification.py - _Defines the classes for each model used in training, it also has the functions for training and storing the data_
        * (12) Identification.py - _This class is used to actually identify where the splash is in an image_
        * (13) Management.py - _Used to save and load models and datasets for all classification and identification tasks_
    * **Scripts:**
        * (14) ImagePrep.py - _short functions to organise images, shrink them and move them also convert them to matrixes_
    * **Settings:**
        * (15) Constants.py - _All contants and paths used within the code_
        * (16) CoreClass.py - _Each frame is defined as a class comprising of its OOI and other important information_
    * **VideoControl:**
        * (17) VideoControl.py - _This allows for pausing, playing, quiting and any other controls during playback_

## Machine Learning ##
### Prediction Methods ###
#### Random Forrest ####
#### Linear Regression ####
#### Neural Networks ####
### Action Methods ###
#### Random Choice ####
#### Largest Projected Growth ####
#### Reinforcement Learning ####

## Code Details ##


### Required Library ###
For this code to work we need to a user will need to ensure the following libraries are installed.

| Library        | Use          |
| :-------------: |-------------|
| numpy | Matrix calculations |
| cv2 (openCV) | All image processing|
| pandas | df storage|
| Tensor Flow | Machine learning|
| time | measure time for processes to run|
| PIL | Image manipulation and extraction|
| os | path manipulation|
| sklearn | Machine Learning Modelling and validation|
| csv | output files of data|
| ctypes | pop ups|
| pickle | saving models|
| pathlib | selecting paths and manipulating them|
| seaborn | graphing heat map|
| matplotlib | graphing|
| sys | controlling output to allow progress bars|


## To Be ##
### Potential Improvements ###
* Target identification can be improved by using I.R. or utilising another technology to extract it more clearly

### Key Considerations and Risks ###
Going forward the following should be resolved or at least considered prior to starting the engagement. this will ensure no issues will arise later

|Risk	|Description	|Mitigation Option (s)|
|:-------------: |-----------------|-------------|
|Identifying the target|Currently my model estimates the target based on the tow rope, this is problematic as it is inaccurate and often completely wrong, also it does not work for ropes that canâ€™t really be seen.|Implement identifying attribute on the target, so the colour can be extracted easily. This will be required sooner rather than later as it will otherwise limit automation effectiveness|
|2 video sources (line and rake)|This PoC was only able to address one data source. The process can be applied to the second, but data collection and model building will take a lot of time.|Need the VA implementation to be longer and consider this restriction as being able to breakdown one video type is only half the job.|
|Ability to work on poorer quality video|Based on a lot of the video I have seen only really the good quality video will be able to be automated. This is expected as it is near impossible for humans to see in some of the video. |Communicate this limitation clearly|
|Generalising (Models work for a range of data sets)|A concern in all data science work is the ability for the models to work on unseen data. The PoC has indicated the models can generalise at this point but there is potential that when we go to implement this it will not work perfectly and may not meet client expectations.|Communicate this limitation clearly|
