# Chapter 8: AI in Motion — Rehabilitation, Wearables and Robotics

## Opening Case
Six weeks after his knee injury, Karim is in rehabilitation. He cannot afford to travel to the clinic three times a week. So his physiotherapist sets up a home programme. Twice a week, Karim films himself squatting with his phone. An app tracks his hips, knees and ankles and reports his knee angle. A wrist band counts his steps.

At the video review, the app says 95° of knee bend. But the squat clearly looks shallower. His trousers are baggy and the room is dark. The physiotherapist measures his knee with a goniometer: 80°. She adjusts his programme.

Movement is data too. How do cameras and sensors turn movement into numbers? How far can we trust them?

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Describe how pose estimation turns video into joint angles.
2. [LO2] Explain how wearable sensors measure movement, and their limits.
3. [LO3] Judge the evidence for remote rehabilitation and home-exercise apps.
4. [LO4] Distinguish the levels of autonomy in medical robots.
5. [LO5] Describe how AI measures surgical skill and where self-operating robots stand.

> **Medical Background in 60 Seconds:** The **gait cycle** is one full step, from one heel strike to the next heel strike of the same foot. **Range of motion** is how far a joint can move, measured in degrees with a goniometer. After a knee injury, physiotherapists track movement, strength and walking to guide recovery.

## 8.1 Pose Estimation: From Video to Joints
**Pose estimation** means finding points on the body, such as hips, knees and ankles, in each video frame. Joining the points makes a stick figure. Software then calculates joint angles and walking speed (Figure 8.1).

OpenPose is a widely used system for this [1]. Researchers have used such tools on ordinary phone videos to measure walking [2]. This could bring gait assessment outside special laboratories.

![Figure 8.1 — Pose estimation](figures/pose-skeleton.svg)
*Figure 8.1 — The model finds body points in each frame; joint angles are worked out from the lines between them. Illustrative.*

Accuracy depends on conditions. Baggy clothes hide joints. Poor light, one camera angle and a body partly out of view all add error. Most models learned from people walking normally. Walking aids, amputations and unusual movement may not be well covered. Karim's case shows these limits.

## 8.2 Wearables: Sensors on the Body
**Wearable** devices include wrist bands, smartwatches and clip-on sensors. Most contain an **inertial measurement unit** (IMU). It combines an accelerometer and a gyroscope, which record movement and rotation. Software turns these signals into steps, activity or sleep.

Consumer devices count steps fairly well in healthy people [3]. They are less accurate at slow walking speeds and with walking aids. These are exactly the patients many physiotherapists treat. So a device should be checked in the patient group that will use it.

## 8.3 Remote Rehabilitation and Home Apps
**Telerehabilitation** means physiotherapy delivered remotely, often by video. A review found that live video rehabilitation for muscle and joint problems improved function about as much as in-person care [4].

AI can add feedback. Apps can count repetitions, check movement quality and remind patients to exercise. The evidence for these apps is still growing. Judge each app with the Chapter 4 questions: Does it measure what it claims? In whom was it tested? Does it help patients?

A **robotic exoskeleton** is a powered frame worn on the legs. It helps people practise walking after a stroke or spinal injury. Trials so far are small [5]. Exoskeletons support therapists; they do not replace them.

## 8.4 Robots in the Operating Room
In robot-assisted surgery, the surgeon sits at a console and controls instruments inside the patient. This is called **leader–follower telemanipulation**: the surgeon's hands lead, and the robot's arms follow.

The robot adds helpful features:

- *Motion scaling* turns a large hand movement into a tiny instrument movement.
- *Tremor filtering* removes the small natural shake of human hands.
- *Wristed instruments* bend like a wrist inside the body.

In joint replacement, some robots use a **haptic boundary**. The cutting tool can move only inside a planned zone, which protects nearby tissue.

## 8.5 Levels of Autonomy
Most surgical robots today have no autonomy. Every movement comes from the surgeon. A common framework describes six levels [6]:

| Level | Meaning | Example |
|---|---|---|
| 0 | No autonomy | Standard leader–follower robot |
| 1 | Robot assistance | Tremor filtering, haptic boundaries |
| 2 | Task autonomy | Robot does one task, such as stitching, under supervision |
| 3 | Conditional autonomy | Robot plans a task; human approves |
| 4 | High autonomy | Robot decides; human can step in |
| 5 | Full autonomy | No human involved |

A research robot called STAR stitched pig bowel with little human help [7]. This was a small animal study in one laboratory. It shows what may be possible, not readiness for patients.

## 8.6 Measuring Skill
Movement data can also assess people. The **Objective Structured Assessment of Technical Skills** (OSATS) is a rating scale for surgical skill [8]. AI can now study instrument movements and surgical video to estimate skill. The same idea works in rehabilitation: movement quality can be measured and tracked over time.

> **Through Four Lenses**
> - **Medicine:** Doctors should know that most surgical robots today are level 0 or 1. Consent talks should explain who controls the instrument.
> - **Pharmacy:** Pharmacists can combine activity data with medicine reviews. Fewer daily steps after a new sedating drug can signal a problem.
> - **Physical Therapy:** Physiotherapists should check app and wearable measures against clinical tests. Clothing, light and slow walking all reduce accuracy.
> - **Health Sciences:** Technical staff maintain sensors, cameras and robots. Software updates and device changes can shift measurements and should be logged.

> **Myth vs Evidence:** Myth: "Self-operating surgical robots already beat surgeons." Evidence: The best-known result, STAR, was a small study in pigs [7]. Robots used on patients today are controlled by surgeons.

> **Safety Alert:** When an app's measurement disagrees with what you see, measure it yourself. Do not progress exercises or clear a patient for work based on an unchecked app number.

## Key Takeaways
- Pose estimation turns video into joint angles; clothing, light and body type affect accuracy.
- Wearables count steps well in healthy walkers, less well in slow or assisted walking.
- Live video rehabilitation for muscle and joint problems works about as well as in-person care.
- Surgical robots today are mostly controlled by surgeons, with helpful features, not self-operating.
- Every movement measure must be checked in the people who will use it.

## Self-Assessment
**Q1.** An app finds Karim's hips, knees and ankles in each video frame. What is this called? [LO1]
A) Pose estimation
B) Retrieval-augmented generation
C) Pharmacovigilance
D) Triage

**Q2.** Karim's app says 95°, but a goniometer shows 80°. He wore baggy trousers in a dark room. What is the most likely cause? [LO1]
A) The goniometer is always wrong.
B) Someone attacked the app.
C) Clothing and poor light reduced the app's accuracy.
D) His knee changed during the call.

**Q3.** An 80-year-old with a walking frame wears a step counter. What should the physiotherapist expect? [LO2]
A) Perfect step counts
B) Possible undercounting, because slow assisted walking reduces accuracy
C) Overcounting of calories only
D) No data at all

**Q4.** What is inside an inertial measurement unit? [LO2]
A) A camera and a microphone
B) A thermometer and an oxygen sensor
C) A magnet and radio coils
D) An accelerometer and a gyroscope

**Q5.** What does a review say about live video rehabilitation for muscle and joint problems? [LO3]
A) It is harmful.
B) It works only for children.
C) It improves function about as much as in-person care.
D) It has never been studied.

**Q6.** What does motion scaling do in robot-assisted surgery? [LO4]
A) Turns a large hand movement into a tiny instrument movement
B) Lets the robot operate alone
C) Measures the patient's blood pressure
D) Records the operation for billing

**Q7.** A robot stitches by itself while the surgeon supervises. Which autonomy level is this? [LO4]
A) Level 0
B) Level 1
C) Level 5
D) Level 2

**Q8.** How should the STAR robot's results be understood? [LO5]
A) STAR is approved for routine human surgery.
B) It is an early animal study showing what may be possible.
C) It proves robots are safer than surgeons.
D) It shows full autonomy in patients.

**Q9.** What is OSATS? [LO5]
A) A robot
B) A drug database
C) A rating scale for surgical skill
D) A wearable sensor

**Q10.** A clinic plans an AI home-exercise app for older patients after hip surgery. What should it check first? [LO3]
A) Whether the app was tested in patients like theirs and improves outcomes
B) Whether the app has nice colours
C) Whether it uses the newest AI
D) Whether it can replace all visits

**Case Question.** Write a short note for Karim's record explaining the gap between the app and the goniometer, its cause and how you will use the app safely.

## Answers and Rationales
**Q1. A** — Finding body points in video is pose estimation [1]. B, C and D are unrelated.

**Q2. C** — Loose clothes and poor light hide joints and add error. A, B and D are unlikely.

**Q3. B** — Step counters are less accurate with slow, assisted walking [3]. A overstates. C and D are wrong.

**Q4. D** — An IMU combines an accelerometer and a gyroscope. A, B and C are other devices.

**Q5. C** — Function improved about as much as standard care [4]. A, B and D are false.

**Q6. A** — Motion scaling makes movements smaller and more precise. B, C and D are not what it does.

**Q7. D** — One task under supervision is level 2 [6]. A has no autonomy. B is assistance only. C has no human.

**Q8. B** — STAR was a small study in pigs [7]. A, C and D overstate it.

**Q9. C** — OSATS is a skill rating scale [8]. A, B and D are wrong.

**Q10. A** — Testing in the right patients and proof of benefit come first. B, C and D do not show safety.

**Case Question — model answer.** "App knee bend 95°; goniometer 80° in the same session. The gap is likely due to loose clothing and low light. The goniometer value is recorded. Next time, Karim will film in good light, wear shorts and keep his whole body in view. I will check the app against a goniometer at each review."

## References
1. Cao Z, Hidalgo G, Simon T, Wei SE, Sheikh Y. OpenPose: realtime multi-person 2D pose estimation using part affinity fields. IEEE Trans Pattern Anal Mach Intell. 2021;43(1):172-186. DOI: 10.1109/TPAMI.2019.2929257
2. Stenum J, Rossi C, Roemmich RT. Two-dimensional video-based analysis of human gait using pose estimation. PLoS Comput Biol. 2021;17(4):e1008935. DOI: 10.1371/journal.pcbi.1008935
3. Fuller D, Colwell E, Low J, et al. Reliability and validity of commercially available wearable devices for measuring steps, energy expenditure, and heart rate: systematic review. JMIR Mhealth Uhealth. 2020;8(9):e18694. DOI: 10.2196/18694
4. Cottrell MA, Galea OA, O'Leary SP, Hill AJ, Russell TG. Real-time telerehabilitation for the treatment of musculoskeletal conditions is effective and comparable to standard practice: a systematic review and meta-analysis. Clin Rehabil. 2017;31(5):625-638. DOI: 10.1177/0269215516645148
5. Louie DR, Eng JJ. Powered robotic exoskeletons in post-stroke rehabilitation of gait: a scoping review. J Neuroeng Rehabil. 2016;13:53. DOI: 10.1186/s12984-016-0162-5
6. Yang GZ, Cambias J, Cleary K, et al. Medical robotics—regulatory, ethical, and legal considerations for increasing levels of autonomy. Sci Robot. 2017;2(4):eaam8638. DOI: 10.1126/scirobotics.aam8638
7. Saeidi H, Opfermann JD, Kam M, et al. Autonomous robotic laparoscopic surgery for intestinal anastomosis. Sci Robot. 2022;7(62):eabj2908. DOI: 10.1126/scirobotics.abj2908
8. Martin JA, Regehr G, Reznick R, et al. Objective structured assessment of technical skill (OSATS) for surgical residents. Br J Surg. 1997;84(2):273-278. DOI: 10.1046/j.1365-2168.1997.02502.x
