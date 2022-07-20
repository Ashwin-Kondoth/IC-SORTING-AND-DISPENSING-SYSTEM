# IC-SORTING-AND-DISPENSING-SYSTEM
## INTRODUCTION
ICs can be difficult to identify and sort if their part numbers are faded out due to
repetitive use. The main aim of this project is to provide new technology application for the 
society. This is a Raspberry pi based vending machine that sorts and dispenses different type 
of ICs. It is mainly focused on segregating each IC based on its part number printed on the IC 
and dispenses it based on the user requirement.
## OBJECTIVES OF THE PROJECT
1. To Identify Integrated circuits.
2. To Sort Integrated circuits. 
3. To Vend Integrated circuits. 
## Objective 1: To Identify Integrated circuits. 
![image](https://user-images.githubusercontent.com/109571829/180017811-e0b89ed4-64f3-4835-a6e7-34aa3f163832.png)

 The proposed design will start by loading different IC’s which are 
  placed on a DC belt drive controlled using L298N DC motor controller.
  
 The belt drive is made to stop precisely such that the IC to be scanned is exactly 
  below the camera using an IR sensor.
  
 The camera takes a snapshot of the IC to be scanned and is sent for text extraction 
  using google vision API.
  
 The extracted text is received by the Raspberry pi.

 String manipulation is done on the text to extract only the numbers, so as to achieve 
  the part number of the IC.
  
 The part number is then used to search the database which was created beforehand 
  to get the name of the IC.
  
## Objective 2: To Sort Integrated Circuits.
![image](https://user-images.githubusercontent.com/109571829/180048631-2d4f1528-84cc-40b1-9bce-c1f92393ed00.png)

The secon objective will start by searching for the angle corresponding 
to the part number detected inside the database.

 Based on the database output the Raspberry pi controls the stepper motor.

 Raspberry pi uses A4988 driver to interface the stepper motor.

 A Nema 17 stepper Motor has been programmed to rotate for 8 compartments, it 
includes one trash compartment where the IC’s whose part number cannot be 
recognized are dumped.

 Each IC has their own rotational angle based on the IC part number.

 Raspberry pi signals the stepper motor to rotate to the appropriate angle such that the 
IC is stored in one of the rectangular compartments on the rotating storage 
compartment.

## Objective 3: To Vend Integrated Circuits
![image](https://user-images.githubusercontent.com/109571829/180049181-5c24d658-6a58-488c-974d-2c1cceca97f3.png)

The third objective will start by using a barcode scanner to scan the 
barcode of each user.

 Database will be created for the particular user once the scanning takes place.

 Keypad is used to input the IC number.

 Vending of the required IC takes place.

 Once the barcode is scanned again, LCD displays the IC’s to be returned.

 Particular database created for the user will be deleted once the IC’s has been 
returned.

 The database created using barcode scanner eliminates the repetition of the first two 
objectives hence saving a lot of time and power.
