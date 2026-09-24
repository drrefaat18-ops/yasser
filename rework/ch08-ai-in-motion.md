# Chapter 8: AI in Motion — Rehabilitation, Wearables and Robotics

## Opening Case
Six weeks after his knee injury, Karim is doing rehabilitation. He cannot afford to travel to the clinic three times a week, so his physiotherapist sets up a home programme. Twice a week, Karim films himself walking and squatting with his phone. An app tracks the position of his hips, knees and ankles in the video and reports his knee bending angle. A wrist band counts his daily steps.

At the video review, the physiotherapist notices that the app reports 95° of knee bend, but Karim's squat clearly looks shallower. His trousers are baggy, and the room is dark. She measures his knee with a goniometer during the video call: 80°. She adjusts his programme.

Motion is data too. How do cameras and sensors turn movement into numbers? How far can we trust them? And what about robots that move instruments inside the body?

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Describe how pose estimation turns video into joint positions and angles.
2. [LO2] Explain how wearable sensors measure movement, and the limits of their validity.
3. [LO3] Evaluate the evidence for telerehabilitation and AI-supported home programmes.
4. [LO4] Distinguish the levels of autonomy in medical robotics.
5. [LO5] Describe how AI assesses surgical skill and where autonomous systems stand today.

> **Medical Background in 60 Seconds:** The **gait cycle** is the sequence of one step, from one heel strike to the next heel strike of the same foot. It has a stance phase, when the foot is on the ground, and a swing phase. **Range of motion** is how far a joint can move, measured in degrees with a goniometer. After a knee injury, physiotherapists track range of motion, strength and gait to guide recovery.

## 8.1 Pose Estimation: From Video to Joints
**Pose estimation** is a computer-vision task. A model finds key points on the body, such as shoulders, hips, knees and ankles, in each video frame. Joining the points gives a stick figure. From it, software calculates joint angles, step length and walking speed (Figure 8.1).

OpenPose is a widely used system that finds body key points for several people at once [1]. Researchers have applied such tools to ordinary two-dimensional videos of walking and obtained useful gait measures [2]. In children with cerebral palsy, a deep-learning model predicted clinical gait parameters from a single camera, which could make assessment possible outside specialised laboratories [3].

![Figure 8.1 — Pose estimation](figures/pose-skeleton.svg)
*Figure 8.1 — A pose-estimation model finds body key points in each video frame; joint angles are calculated from the lines between them. Illustrative.*

The traditional reference method is marker-based motion capture. Reflective markers are placed on the skin, and several cameras track them in a laboratory. When markerless and marker-based systems were compared in the same walkers, differences were a few degrees for most joint angles, but larger for some rotations [4].

Performance depends on conditions. Baggy clothing hides joints. Poor light, a single camera angle and people partly out of view all add error. Most models were trained on people standing and walking normally. Walking aids, amputations, obesity and unusual movement patterns may not be well represented. Karim's case shows these limits.

## 8.2 Wearables: Sensors on the Body
**Wearable** devices include wrist bands, smartwatches and sensors clipped to the body. Most contain an **inertial measurement unit** (IMU), which combines an accelerometer and a gyroscope. The IMU records acceleration and rotation many times per second. Algorithms then turn these signals into steps, activity type, sleep or joint angles.

Consumer devices count steps reasonably well in controlled tests, but they are less accurate for energy expenditure [5]. They are also less accurate at slow walking speeds and in people who use walking aids. These are exactly the people many physiotherapists treat. A device validated in healthy young adults may undercount steps in an older patient with a limp.

Wearables become clinically useful when they are validated for the patient group and the measure that matters. Examples include step counts after surgery, time spent upright in hospital and fall detection in older adults.

## 8.3 Telerehabilitation and Home Programmes
**Telerehabilitation** delivers physiotherapy remotely, often by video. A systematic review of real-time telerehabilitation for musculoskeletal conditions found improvements in physical function that were comparable to standard in-person care [6].

AI adds automated feedback. Apps can count repetitions, check movement quality and remind patients to exercise. This may help adherence, which is a major problem in rehabilitation. The evidence for AI-feedback apps is still developing, and each app should be judged by the questions in Chapter 4. Does it measure what it claims? In whom was it tested? Does it improve outcomes?

A **robotic exoskeleton** is a powered frame worn on the legs. It supports stepping practice after stroke or spinal cord injury. A review found that exoskeletons are promising but that trials are small and methods vary [7]. They support therapists; they do not replace them.

> **Deeper Dive:** An accelerometer measures acceleration in three directions. When a person walks, each heel strike produces a spike in the signal. A step-counting algorithm finds these spikes. It must ignore spikes from other movements, such as waving a hand. A slow, shuffling walk produces smaller spikes that may fall below the algorithm's threshold, so steps are missed.

## 8.4 Robots in the Operating Room
In robot-assisted surgery, the surgeon sits at a console and controls instruments inside the patient. This arrangement is called **leader–follower telemanipulation**: the surgeon's hand movements lead, and the robot's arms follow.

The robot adds several features.

- **Motion scaling** turns a large hand movement into a small instrument movement, for precision.
- **Tremor filtering** removes the natural small shake of human hands. Physiological tremor occurs at about 8–12 Hz, so the system filters movements at those frequencies.
- Wristed instruments bend like a wrist inside the body. The instrument system has seven degrees of freedom, compared with four for a rigid laparoscopic instrument.

In orthopaedic surgery, some robots use a **haptic boundary**. The system allows the cutting tool to move only within a planned zone, which protects surrounding tissue during joint replacement.

## 8.5 Levels of Autonomy
Most surgical robots today have no autonomy: every movement comes from the surgeon. A widely used framework describes six levels [8]:

| Level | Description | Example |
|---|---|---|
| 0 | No autonomy | Standard leader–follower robot |
| 1 | Robot assistance | Tremor filtering, haptic boundaries |
| 2 | Task autonomy | Robot performs a specific task, such as suturing, under supervision |
| 3 | Conditional autonomy | Robot plans and performs a task; human approves and monitors |
| 4 | High autonomy | Robot makes decisions; human can intervene |
| 5 | Full autonomy | No human involved |

The Smart Tissue Autonomous Robot (STAR) sewed together two ends of pig bowel with little human help. Its stitches were more consistent than those of surgeons in the same experiment [9]. This was a preclinical study in a small number of animals in one laboratory. It shows feasibility, not readiness for patients.

## 8.6 Measuring Skill
Motion data can also assess people. The **Objective Structured Assessment of Technical Skills** (OSATS) is a rating scale for surgical skill, developed at the University of Toronto [10]. AI systems now analyse instrument movements and surgical video to estimate skill automatically, for example by measuring economy of motion. **Surgical data science** is the wider field that collects and analyses such data to improve care [11].

The same idea applies in rehabilitation. Movement quality can be measured, tracked over time and fed back to the patient.

> **Through Four Lenses**
> - **Medicine:** Physicians should know that robotic systems today are mostly level 0 or 1. Consent discussions should explain who controls the instrument and what the robot does automatically.
> - **Pharmacy:** Pharmacists can combine activity data with medicine reviews. A drop in daily steps after starting a sedating drug, or dizziness after a blood-pressure change, can signal a problem worth acting on.
> - **Physical Therapy:** Physiotherapists should validate pose and wearable measures against clinical tests in their own patients. Clothing, light, walking aids and slow gait all reduce accuracy.
> - **Health Sciences:** Biomedical and technical staff maintain sensors, cameras and robots. Calibration, software updates and device changes can shift measurements, and should be logged and checked.

> **Myth vs Evidence:** Myth: "Autonomous surgical robots already outperform surgeons." Evidence: The best-known autonomous result, STAR, was a small preclinical study in pigs [9]. Robots in clinical use today are controlled by surgeons.

> **Safety Alert:** When an app's movement measure disagrees with what you see, measure it yourself. Do not progress exercises, clear a patient to return to work or record a result based on an unchecked app number.

## Key Takeaways
- Pose estimation turns video into joint positions and angles; accuracy depends on clothing, light and body type.
- Wearables use IMUs; step counts are reasonable in healthy walkers but less accurate in slow or assisted walking.
- Real-time telerehabilitation for musculoskeletal conditions gives results comparable to in-person care.
- Surgical robots today are mostly leader–follower systems with assistance features, not autonomous surgeons.
- AI can measure skill and movement quality, but each measure must be validated in the people who use it.

## Self-Assessment
**Q1.** An app finds the positions of Karim's hips, knees and ankles in each frame of a video. What is this task called? [LO1]
A) Pose estimation
B) Retrieval-augmented generation
C) Pharmacovigilance
D) Computer-aided triage

**Q2.** Karim's app reports 95° of knee bend, but a goniometer shows 80°. He wore baggy trousers in a dark room. What is the most likely cause? [LO1]
A) The goniometer is always wrong.
B) The app is adversarially attacked.
C) Clothing and poor light reduced pose-estimation accuracy.
D) Karim's knee changed during the call.

**Q3.** An 80-year-old patient using a walking frame wears a consumer step counter. What should the physiotherapist expect? [LO2]
A) Perfect step counts
B) Possible undercounting because slow, assisted walking reduces accuracy
C) Overcounting of energy expenditure only
D) No data at all

**Q4.** What does an inertial measurement unit contain? [LO2]
A) A camera and a microphone
B) A thermometer and a pulse oximeter
C) A magnet and radio coils
D) An accelerometer and a gyroscope

**Q5.** What does a systematic review report about real-time telerehabilitation for musculoskeletal conditions? [LO3]
A) It is harmful.
B) It works only for children.
C) It improves physical function comparably to in-person care.
D) It has never been studied.

**Q6.** A robot filters the surgeon's hand tremor. Which frequency range does it target? [LO4]
A) About 8–12 Hz
B) About 0.1–0.5 Hz
C) About 50–60 Hz
D) About 200–300 Hz

**Q7.** A robot performs a specific suturing task by itself while the surgeon supervises. Which autonomy level is this? [LO4]
A) Level 0
B) Level 1
C) Level 5
D) Level 2

**Q8.** What is the correct interpretation of the STAR robot's bowel-suturing results? [LO5]
A) STAR is approved for routine human surgery.
B) It is a preclinical proof of feasibility in a small number of animals.
C) It proves robots are safer than surgeons.
D) It shows full (level 5) autonomy in patients.

**Q9.** What is OSATS? [LO5]
A) A robot model
B) A drug-safety database
C) A rating scale for surgical technical skill
D) A wearable sensor

**Q10.** A clinic plans to use an AI home-exercise app for older patients after hip surgery. What should it check first? [LO3]
A) Whether the app was validated in patients like theirs and improves outcomes
B) Whether the app has a pleasant colour scheme
C) Whether the app uses the newest neural network
D) Whether the app can replace all clinic visits

**Case Question.** Write a short note for Karim's record explaining the difference between the app's knee angle and your goniometer measurement, what caused it, and how you will use the app safely in future sessions.

## Answers and Rationales
**Q1. A** — Finding body key points in video is pose estimation [1]. B, C and D are unrelated tasks.

**Q2. C** — Loose clothing and poor light hide joint landmarks and add error. A is false. B is deliberate manipulation, not present here. D is implausible.

**Q3. B** — Step counters are less accurate at slow speeds and with walking aids [5]. A overstates. C and D are wrong.

**Q4. D** — An IMU combines an accelerometer and a gyroscope. A, B and C describe other devices.

**Q5. C** — Function improved comparably to standard care [6]. A, B and D are false.

**Q6. A** — Physiological tremor is about 8–12 Hz. B, C and D are wrong ranges.

**Q7. D** — Performing a specific task under supervision is task autonomy, level 2 [8]. A has no autonomy. B is assistance only. C involves no human.

**Q8. B** — STAR was tested in a small number of pigs in one laboratory [9]. A, C and D overstate the evidence.

**Q9. C** — OSATS is a surgical skill rating scale [10]. A, B and D are wrong.

**Q10. A** — Validation in the target group and evidence of benefit come first. B and C do not show safety. D overreaches.

**Case Question — model answer.** "App-reported knee flexion 95°; goniometer measurement 80° in the same session. The difference is likely due to loose clothing and low light, which reduce pose-estimation accuracy. The goniometer value is recorded as the reference. For future sessions, Karim will film in good light, wear shorts and keep his whole body in view. I will check the app against a goniometer measurement at each review until the two agree consistently."

## References
1. Cao Z, Hidalgo G, Simon T, Wei SE, Sheikh Y. OpenPose: realtime multi-person 2D pose estimation using part affinity fields. IEEE Trans Pattern Anal Mach Intell. 2021;43(1):172-186. DOI: 10.1109/TPAMI.2019.2929257
2. Stenum J, Rossi C, Roemmich RT. Two-dimensional video-based analysis of human gait using pose estimation. PLoS Comput Biol. 2021;17(4):e1008935. DOI: 10.1371/journal.pcbi.1008935
3. Kidziński Ł, Yang B, Hicks JL, et al. Deep neural networks enable quantitative movement analysis using single-camera videos. Nat Commun. 2020;11:4054. DOI: 10.1038/s41467-020-17807-z
4. Kanko RM, Laende EK, Davis EM, Selbie WS, Deluzio KJ. Concurrent assessment of gait kinematics using marker-based and markerless motion capture. J Biomech. 2021;127:110665. DOI: 10.1016/j.jbiomech.2021.110665
5. Fuller D, Colwell E, Low J, et al. Reliability and validity of commercially available wearable devices for measuring steps, energy expenditure, and heart rate: systematic review. JMIR Mhealth Uhealth. 2020;8(9):e18694. DOI: 10.2196/18694
6. Cottrell MA, Galea OA, O'Leary SP, Hill AJ, Russell TG. Real-time telerehabilitation for the treatment of musculoskeletal conditions is effective and comparable to standard practice: a systematic review and meta-analysis. Clin Rehabil. 2017;31(5):625-638. DOI: 10.1177/0269215516645148
7. Louie DR, Eng JJ. Powered robotic exoskeletons in post-stroke rehabilitation of gait: a scoping review. J Neuroeng Rehabil. 2016;13:53. DOI: 10.1186/s12984-016-0162-5
8. Yang GZ, Cambias J, Cleary K, et al. Medical robotics—regulatory, ethical, and legal considerations for increasing levels of autonomy. Sci Robot. 2017;2(4):eaam8638. DOI: 10.1126/scirobotics.aam8638
9. Saeidi H, Opfermann JD, Kam M, et al. Autonomous robotic laparoscopic surgery for intestinal anastomosis. Sci Robot. 2022;7(62):eabj2908. DOI: 10.1126/scirobotics.abj2908
10. Martin JA, Regehr G, Reznick R, et al. Objective structured assessment of technical skill (OSATS) for surgical residents. Br J Surg. 1997;84(2):273-278. DOI: 10.1046/j.1365-2168.1997.02502.x
11. Maier-Hein L, Vedula SS, Speidel S, et al. Surgical data science for next-generation interventions. Nat Biomed Eng. 2017;1(9):691-696. DOI: 10.1038/s41551-017-0132-7
