# Chapter 9: Monitoring, Prediction and Population Health

## Opening Case
Amal is in hospital with a urine infection. At 3 a.m., the ward computer shows an alert: "High risk of getting worse in the next 12 hours." Her heart rate has crept up. Her blood pressure has drifted down. Her creatinine is rising.

The night nurse has already seen three alerts tonight. Two were false alarms. She checks Amal herself. Amal is confused and her skin is cool. The nurse calls the doctor, who starts fluids. By morning, Amal is better.

Prediction models promise early warning. But every alert takes time. When does a warning help, and when does it become noise?

## Learning Objectives
By the end of this chapter you will be able to:
1. [LO1] Explain how early-warning models work and why they create many alarms.
2. [LO2] Weigh early warning against false alarms.
3. [LO3] Describe AI that reads the ECG and the trial evidence behind it.
4. [LO4] Describe automatic insulin delivery and who it is for.
5. [LO5] Judge a population-health AI claim using the lesson of Google Flu Trends.

> **Medical Background in 60 Seconds:** **Sepsis** is a life-threatening reaction to infection that damages the body's own organs. Early signs include fast breathing, fast pulse, low blood pressure and confusion. **Acute kidney injury** (AKI) is a sudden fall in kidney function, often seen as rising creatinine. Both are easier to treat when caught early.

## 9.1 Early Warning: From Scores to Models
Hospitals have long used an **early warning score**. Nurses record vital signs, and each value earns points. The National Early Warning Score (NEWS2) is widely used [1]. A high total triggers a review. It is a simple, rule-based system.

Machine-learning models go further. They use many more inputs, such as laboratory results and trends over time. They aim to warn earlier.

The TREWS sepsis system was studied in five hospitals [2]. When doctors confirmed its alert within three hours, fewer patients died. This was not a randomised trial, but it is fairly strong evidence.

Not every tool works as claimed. A popular commercial sepsis model, tested independently, missed two-thirds of cases (Chapter 4) [3].

## 9.2 Early Warning Versus False Alarms
A model can warn early or warn accurately. Doing both is hard. Warning earlier means using weaker signals, which gives more false alarms.

One well-known model predicted AKI up to 48 hours early [4]. It caught 90% of the most severe cases. But for every true alert, it gave about two false ones. Also, 93.6% of patients in its data were men. How well it works for women was unclear.

On a busy ward, many false alerts add up. Each one needs a nurse to check the patient. If staff lose trust, they start ignoring alerts. This is **alarm fatigue**. Before using a model, ask: How many alerts per shift? Who responds, and what do they do?

## 9.3 AI and the ECG
The **electrocardiogram** (ECG) records the heart's electrical activity. It is cheap and available almost everywhere. AI can find patterns in the ECG that people cannot see.

One model spotted people at risk of atrial fibrillation, an irregular rhythm linked to stroke, from an ECG with a normal rhythm [5]. Another finds a weak heart pump from a standard ECG.

That second model was tested in a randomised trial with over 22,000 patients [6]. Teams that saw the AI result found more cases of weak heart pump: 2.1% of patients instead of 1.6%. The benefit was real but modest. This is a realistic picture: AI helps, but often less than accuracy figures suggest.

![Figure 9.1 — Trend-based instability prediction](../images/image14.png)
*Figure 9.1 — A sketch of blood pressure over time. A model flags a subtle trend before pressure clearly falls.*

## 9.4 Automatic Insulin Delivery
People with **type 1 diabetes** make no insulin and must replace it every day. A **closed-loop system** links a glucose sensor, a computer program and an insulin pump (Figure 9.2). The sensor measures glucose every few minutes. The program adjusts insulin automatically.

In a six-month randomised trial, closed-loop systems raised the time spent in the healthy glucose range from 59% to 71% of the day [7].

![Figure 9.2 — Closed-loop insulin delivery](figures/orig-image18.png)
*Figure 9.2 — A glucose sensor feeds a dosing program, which adjusts an insulin pump.*

Amal has type 2 diabetes and takes tablets, not insulin. This tool is not for her current treatment. Knowing who a tool is for is part of using it safely.

## 9.5 Population Health
Public health watches whole communities. AI helps by scanning news, social media and health records for signs of outbreaks [8].

Google Flu Trends teaches an important lesson. In 2009, flu-related web searches tracked official flu reports closely [9]. For a few years, it looked like a cheap way to track flu. Then it failed. In 2012–2013, it predicted more than double the real level [10].

Why? People's search habits changed, and media stories about flu made healthy people search too. The model had no link to the biology of flu. This is distribution shift and shortcut learning on a national scale (Chapter 3).

> **Through Four Lenses**
> - **Medicine:** Doctors should know how often an alert is right and how early it warns. An alert should prompt a bedside review, not automatic treatment.
> - **Pharmacy:** Pharmacists can act on kidney alerts by reviewing doses of kidney-cleared drugs. Early medicine review can prevent the injury the model predicts.
> - **Physical Therapy:** Physiotherapists can use monitoring data to time exercise safely. Falling blood pressure may mean waiting, while stable trends support earlier movement.
> - **Health Sciences:** Public-health officers should compare digital signals with laboratory-confirmed data. Laboratory results give surveillance models real biological meaning.

> **Myth vs Evidence:** Myth: "Big data can replace traditional disease surveillance." Evidence: Google Flu Trends first tracked flu well [9], but later more than doubled the true level [10]. Digital signals work best alongside laboratory data.

> **Safety Alert:** An alert is a prompt to look at the patient, not a diagnosis. No alert does not mean no problem. If a patient looks unwell, act.

## Key Takeaways
- Early-warning scores use simple rules; AI models use more data and aim to warn earlier.
- Earlier warnings bring more false alarms; alarm burden decides whether a model helps.
- ECG AI has trial evidence of real but modest benefit.
- Automatic insulin delivery improves glucose control in type 1 diabetes.
- Population AI can fail when behaviour changes, as Google Flu Trends showed.

## Self-Assessment
**Q1.** NEWS2 adds points for vital signs such as breathing rate and pulse. What kind of system is it? [LO1]
A) A deep-learning model
B) A rule-based early warning score
C) A large language model
D) An automatic insulin system

**Q2.** A kidney model warns 48 hours early but gives two false alerts for every true one. What is the main practical concern? [LO2]
A) It cannot find severe cases.
B) Its data were too large.
C) It uses creatinine.
D) Staff workload and alarm fatigue from false alerts

**Q3.** The same model was trained on patients who were 93.6% men. What should a hospital do first? [LO2]
A) Check how it performs in women and in its own patients
B) Use it only at night
C) Use it as it is because the data were large
D) Remove creatinine

**Q4.** In a randomised trial, AI-ECG results raised diagnosis of a weak heart pump from 1.6% to 2.1%. What is the best interpretation? [LO3]
A) The AI replaced heart scans.
B) The AI had no effect.
C) The AI gave a real but modest benefit.
D) The AI caused heart failure.

**Q5.** An AI model spots atrial fibrillation risk from an ECG with a normal rhythm. What does this show? [LO3]
A) The ECG was faulty.
B) AI can find ECG patterns that people cannot see.
C) Atrial fibrillation is not linked to stroke.
D) The model uses age only.

**Q6.** Who is an automatic (closed-loop) insulin system designed for? [LO4]
A) A person with type 1 diabetes who uses insulin
B) Amal, who takes tablets for type 2 diabetes
C) A person with high blood pressure only
D) A patient with a knee injury

**Q7.** What did closed-loop insulin delivery improve in a six-month trial? [LO4]
A) Blood pressure
B) Kidney function
C) Weight only
D) Time spent in the healthy glucose range

**Q8.** Why did Google Flu Trends fail? [LO5]
A) No one searched for flu any more.
B) Laboratory tests stopped.
C) Search habits and media stories changed, so the link to real flu shifted.
D) The model was too small.

**Q9.** An app claims to track an outbreak from social-media posts. How should it be judged? [LO5]
A) Compare its signal over time with laboratory-confirmed data
B) Count how many posts it reads
C) Trust it if it uses AI
D) Check if it has a colourful map

**Q10.** A ward gets 6 alerts a day, and 2 are true. What share of alerts are real? [LO1]
A) 12%
B) 66%
C) 50%
D) 33%

**Case Question.** The ward manager wants to switch off the alerts because "most are false". Write a short reply explaining the trade-off and suggesting one change.

## Answers and Rationales
**Q1. B** — NEWS2 adds points with fixed rules [1]. A, C and D are other tools.

**Q2. D** — Frequent false alerts cause workload and fatigue [4]. A is false. B and C are not concerns.

**Q3. A** — A model trained mostly on men must be checked in women and local patients. B, C and D miss the problem.

**Q4. C** — The trial showed a real but modest gain [6]. A, B and D misread it.

**Q5. B** — AI detects subtle patterns people miss [5]. A, C and D are false.

**Q6. A** — These systems are for insulin users with type 1 diabetes [7]. B, C and D are not the users.

**Q7. D** — Time in range rose from 59% to 71% [7]. A, B and C were not the main result.

**Q8. C** — Changing behaviour broke the link the model relied on [10]. A, B and D are wrong.

**Q9. A** — Digital signals should be checked against confirmed data. B, C and D do not test accuracy.

**Q10. D** — 2 ÷ 6 = 33%. A, B and C are wrong.

**Case Question — model answer.** "I understand, because false alerts take time from other patients. But the alerts also catch real problems early, as with Amal. Switching them off loses that. Instead, we could ask the informatics team to adjust the threshold so fewer low-value alerts fire, and track how many alerts per shift are real."

## References
1. Royal College of Physicians. National Early Warning Score (NEWS) 2: standardising the assessment of acute-illness severity in the NHS. London: RCP; 2017. https://www.rcp.ac.uk/improving-care/resources/national-early-warning-score-news-2/
2. Adams R, Henry KE, Sridharan A, et al. Prospective, multi-site study of patient outcomes after implementation of the TREWS machine learning-based early warning system for sepsis. Nat Med. 2022;28(7):1455-1460. DOI: 10.1038/s41591-022-01894-0
3. Wong A, Otles E, Donnelly JP, et al. External validation of a widely implemented proprietary sepsis prediction model in hospitalized patients. JAMA Intern Med. 2021;181(8):1065-1070. DOI: 10.1001/jamainternmed.2021.2626
4. Tomašev N, Glorot X, Rae JW, et al. A clinically applicable approach to continuous prediction of future acute kidney injury. Nature. 2019;572(7767):116-119. DOI: 10.1038/s41586-019-1390-1
5. Attia ZI, Noseworthy PA, Lopez-Jimenez F, et al. An artificial intelligence-enabled ECG algorithm for the identification of patients with atrial fibrillation during sinus rhythm: a retrospective analysis of outcome prediction. Lancet. 2019;394(10201):861-867. DOI: 10.1016/S0140-6736(19)31721-0
6. Yao X, Rushlow DR, Inselman JW, et al. Artificial intelligence-enabled electrocardiograms for identification of patients with low ejection fraction: a pragmatic, randomized clinical trial. Nat Med. 2021;27(5):815-819. DOI: 10.1038/s41591-021-01335-4
7. Brown SA, Kovatchev BP, Raghinaru D, et al. Six-month randomized, multicenter trial of closed-loop control in type 1 diabetes. N Engl J Med. 2019;381(18):1707-1717. DOI: 10.1056/NEJMoa1907863
8. Freifeld CC, Mandl KD, Reis BY, Brownstein JS. HealthMap: global infectious disease monitoring through automated classification and visualization of Internet media reports. J Am Med Inform Assoc. 2008;15(2):150-157. DOI: 10.1197/jamia.M2544
9. Ginsberg J, Mohebbi MH, Patel RS, et al. Detecting influenza epidemics using search engine query data. Nature. 2009;457(7232):1012-1014. DOI: 10.1038/nature07634
10. Lazer D, Kennedy R, King G, Vespignani A. The parable of Google Flu: traps in big data analysis. Science. 2014;343(6176):1203-1205. DOI: 10.1126/science.1248506
