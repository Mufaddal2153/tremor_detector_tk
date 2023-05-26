# Tremor Detector

Tremor Detector is an advanced project developed to diagnose and detect different types of tremors in patients. Built on Python Tkinter, Matplotlib for live tremor visualization, and Sklearn for the machine learning model, this project also incorporates Arduino UNO Micro-controller for reading tremor data through serial communication. By analyzing the collected data, Tremor Detector provides accurate diagnoses for three types of tremors: Hand Tremors, Muscle Rigidity, and Knocking.

## About Tremors

Tremors are involuntary rhythmic movements of body parts that can occur at rest or during voluntary movements. They are often associated with various medical conditions and can significantly affect a person's quality of life. In Tremor Detector, we aim to diagnose and differentiate between three common types of tremors:

1. **Hand Tremors:** Hand tremors are characterized by involuntary shaking of the hands and fingers. They can be caused by conditions such as essential tremor, Parkinson's disease, or certain medications.

2. **Muscle Rigidity:** Muscle rigidity refers to stiffness and resistance to movement in the muscles. It can be a symptom of conditions like Parkinson's disease or other neurological disorders.

3. **Knocking:** Knocking refers to repetitive tapping or knocking movements, often observed in conditions such as Parkinson's disease or restless legs syndrome.

## Key Features

- **Real-time Tremor Visualization:** Tremor Detector leverages Matplotlib to provide live visualizations of tremor data, enabling doctors and patients to observe and analyze the tremor patterns in real time.

- **Arduino Integration:** The project incorporates Arduino UNO Micro-controller to establish a connection and collect tremor data from patients via serial communication. This ensures accurate and reliable data acquisition for diagnosis.

- **Machine Learning Model:** Tremor Detector utilizes the power of Sklearn, a popular machine learning library, to develop a robust classification model. The model analyzes the collected tremor data and provides accurate diagnoses for Hand Tremors, Muscle Rigidity, and Knocking.

- **User-friendly Interface:** Built on Python Tkinter, the project offers an intuitive and user-friendly interface that enables easy interaction with the system. Patients can input their data, and doctors can access the diagnosis results conveniently.

## Technologies Used

The Tremor Detector project is built using the following technologies:

- **Python Tkinter:** The Python library utilized for developing the graphical user interface, providing an interactive and user-friendly experience for both patients and doctors.

- **Matplotlib:** A popular data visualization library in Python used for generating live tremor visualizations, helping doctors and patients visualize and analyze the tremor patterns.

- **Sklearn:** Sklearn, or scikit-learn, is a powerful machine learning library in Python. It is employed in Tremor Detector to build a machine learning model that accurately diagnoses tremors based on collected data.

- **Arduino UNO Micro-controller:** The Arduino UNO Micro-controller is integrated into the project to facilitate the collection of tremor data through serial communication, ensuring precise and reliable data acquisition.
