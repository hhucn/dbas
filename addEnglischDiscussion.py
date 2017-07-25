import transaction
import collections

from dbas.database import get_dbas_db_configuration, DBDiscussionSession as session
from dbas.database.discussion_model import TextVersion, Statement, Argument, Premise, PremiseGroup, Issue
from dbas.helper.tests import add_settings_to_appconfig

settings = add_settings_to_appconfig()
session.configure(bind=get_dbas_db_configuration('discussion', settings))

old_issue_uid = 1
new_issue_uid = None
statement_from_old_to_new = {}
statement_from_new_to_old = {}
pgroups_from_old_to_new = {}

data = {
    1: 'we should introduce an admission restriction ',
    2: 'the demand for the course is too large, so that a restriction must be introduced',
    3: 'many students register themselves without having the necessary skills',
    4: 'a comparability of the high school grades is not given',
    5: 'the capacity of the university should be increased instead of excluding new students',
    6: 'the course standards should be increased',
    7: 'the students will receive a professionally higher degree',
    8: 'the number of students can be reduced in a natural way',
    9: 'many students are already dropping out',
    10: 'drop-out rate should not be lowered, but the number of less talented freshmen should be lowered.',
    33: 'previous graduates still have deficits in many areas',
    35: 'students, who do not drop out, have too little knowledge to start their professional life yet',
    36: 'the level of requirement is not printed on the certificates',
    37: 'the secondary school certificate does not contain a lot of information regarding computer science skills, since only a few schools teach computer science in a serious fashion',
    38: 'more lectures should be reworked. In particular lectures in mathematics where there are a lot of problems. Lectures in this area that are specifically tailored to computer science students would be a good idea',
    39: 'I do have the impression (without being able to give specific numbers), that students discontinue their studies more often because of problems with mathematics rather than with computer science',
    40: 'there is a bottleneck here. There are many students from Mathematics, Physics and Computer Science coming together to attend those courses. Offering mathematics courses that are tailored to computer science would also make sense, because they could convey topics that are of special interest for computer scientists and not for mathematicians.',
    41: 'we do not have a sufficient amount of professorships in computer science to offer these additional courses',
    44: 'with the increased number of students we should be able to let computer science professors hold those lectures',
    45: 'only by giving the computer science studies a trial one can determine whether one is suited for these studies',
    46: 'a high demand does not imply that we have to introduce restricted admission',
    47: 'it would reduce the dropout rate',
    48: 'computer science graduates would have better job opportunities since they would be better prepared for those jobs',
    49: 'there should be an admission test for computer science studies since the lack of computer science education in schools renders the school grades irrelevant for admission restrictions',
    50: 'I do not see any other way to determine whether one is able to be successfull at computer science studies',
    51: 'this would reduce the dropout rate since unsuited candidates would be excluded before they start their studies',
    52: 'the timetable for lectures does not work well, in particular this is the case for the exemplary timetable contained in the examination regulations from 2013',
    53: 'there are not enough courses or everything overlaps',
    54: 'we are currently receiving two lectures',
    55: 'one can be used to teach only computer scientists, since we are the second largest course of study',
    56: 'thus also the majority in the lectures',
    57: 'professors do not neccesarily have to be taken from computer science, but also from mathematics',
    58: 'one could also use alternative admission indicators like internships or special grades in subjects of natural science',
    59: 'students often have no way of acquiring the abilities required in the qualification test by themselves',
    60: 'the acquisition of such skills is the task of the study',
    61: 'students often have no or only bad opportunities to acquire the abilities required in the qualitifaction test by themselves',
    62: 'the rising number of freshmen necessitates a form of restriction',
    63: 'freshmen are not yet adapted to the university studies',
    64: 'a suitability can not be clearly ascertained',
    65: 'the secondary school certificate refers only to a small extent to relevant fields',
    66: 'it is not meaningful',
    67: 'there are probably many students who are not aware of their competencies and therefore they need an orientation',
    68: 'The compulsory mathematics lectures contain the necessary foundations for later studies, which are difficult to combine with didactic correctness into a single module',
    69: 'many students have a minor subject that is either very mathematical or mathematics itself, and therefore need the knowledge conveyed in the compulsory mathematics lectures',
    70: 'the mathematics lectures are already adjusted through low admission criteria ',
    71: 'passing the course without grade already exists for computer scientists',
    72: 'this lecture is also attended by mathematicians and is actually intended for them and therefore can not be adapted to the computer scientists',
    73: 'the current examination regulations provide for about one third of the study for secondary subjects and compulsory subjects, and thus contain too few computer science lectures for a computer science study',
    74: 'the level of requirements is not evenly distributed over the course of study and therefore does not have any influence on the freshmen',
    75: 'at the latest some will reach their limits with math modules or developmental modules which require individual work from them',
    76: 'it only moves students, who enroll solely for the local traffic card, (if at all) to other admission-free subjects',
    77: 'thus, the courses are not used to sort out the students',
    78: 'exercises will not help anyone, if only solutions of the last week are discussed! The exercises should prepare for the next sheet. Just upload solutions und done',
    79: 'students receive help instead of being left on their own',
    80: 'here is a bottleneck. There are many students from mathematics, physics, computer science and other disciplines. A mathematics subject specially designed for computer science would also be useful, because it is possible to convey content that is useful for computer scientists and not for mathematicians',
    81: 'solutions can be easily accessed and understood. New tasks are usually more useful. More complex and important solutions can be discussed anyway, of course',
    82: 'the university should increase its capacities',
    83: 'the number of freshmen has grown considerably in Germany over the last few years',
    84: 'computer scientists with a degree have good job prospects',
    85: 'it is not just about the grades, but about the acquired competencies',
    86: 'the requried skills for a suitability test are not yet specified. For example, a test that requires basic logical understanding does not necessarily require prepared students',
    87: 'students should definitely see the right solutions and it may be helpful to see them get solved live. A preparation for the next sheet will take place already in good practice groups, in addition to a discussion of old tasks. No change is required',
    88: 'the understanding of solutions is not always sufficient. Focus should therefore be on the discussion of old tasks, where in addition particularly complex and important tasks of the next sheet could be discussed, if necessary',
    89: 'not the number of students, but only the number of drop-outs would be increased',
    90: 'these tailored mathematics courses for computer scientists need not neccessarily be held by computer scientists',
    91: 'more professors must be hired to withstand the surge of new students, anyway',
    92: 'which cannot be the norm, because computer scientists also have to be graded for their oh so important achievements in mathematical fields',
    93: 'according to my experience the sample study plans work when you see them as exactly what they are: samples and no prescriptions chiselled in stone',
    94: 'I did not encounter the specified problems thus far. Please justify why there are not enough courses, or how everything overlaps',
    95: 'this occures for example with a minor in biology in the summerterm 2015: If one holds exactly to the sample plan, one has no possibility to reach the necessary points in the fifth semester',
    96: 'this costs money and there are many dropouts. Therefore it would be more sensible and cost-effective to create a better selection process',
    97: 'a lower standard is reached in the mathematical part, rather than a higher one',
    98: 'in the lectures of mathematics the fundamentals of mathematics are taught, but these are the same for all. Specializations belong to the respective courses',
    99: 'a high requirement level has a sorting out effect',
    100: 'the exercise groups are normal sized, so that one can respond to the students\' wishes',
    101: 'when the solutions are only uploaded, the students are also on their own',
    102: 'exercises will not help anyone, if only solutions of the last week are discussed! The exercises should prepare for the next sheet. Just upload solutions and be done',
    103: 'hard does not mean impossible and the basic mathematical principles are not different but nonetheless can be better conveyed if one can directly use application examples from computer science. Thus, this probably increases the motivation of many first-year students',
    104: 'the number of students has increased considerably since the university founding, while the available capacities (in this case, room capacities) have remained relatively unchanged',
    105: 'there are also capacity problems in the higher semesters, where the drop-out rate is much lower than in the first semester',
    106: 'the lecture content, which has to be taught as basics will not fit into a single lecture if new topics are not to be introduced incoherently',
    107: 'it does therefore not make a difference, whether sample solutions are uploaded and tasks requiring presence are discussed or vice versa, since these can be "retrieved and comprehended on one\'s own"',
    111: 'a successful continuation in the study depends, among other things, on factors such as self motivation, discipline and willingness to learn independently, which can not be measured with any selection process',
    112: 'the selection procedures cost time and money as well. There are also many student dropouts in subjects with a restriction on admission',
    113: 'ticket students do not visit the lectures and exercises anyway',
    114: 'the mathematics lectures are completely overcrowded',
    115: 'a closer teaching for computer science would be more sensible',
    116: 'exercises will not help anyone, if only solutions of the last week are discussed! The exercises should prepare for the next sheet. Just upload solutions and be done',
    117: 'I basically do not see the need for an aptitude test',
    118: 'this will be shown in the first semesters anyway',
    119: 'you do not need knowledge of computer science prior to your studies in order to successfully complete them',
    120: 'one can determine the suitability for the study generally only during the study. Many students fail because they lack self-motivation, which is secondary in during school',
    121: 'the demand for computer scientists is also great',
    122: 'the reputation of the university will increase as a result of the skills of its graduates',
    123: 'many students start the study with false expectations of the requirements',
    124: 'sample study schedules are there to show the students how their studies might look. If students find this good ',
    125: 'stick to them or use them as orientation it should not incur any difficulties. In my current semester, almost 6 courses are offered for the mandatory section, I would have liked to take four of them',
    126: 'find that this is absolutely irresponsible towards the students',
    127: 'the reputation of the university is also considerably damaged. Unorganized',
    128: 'which is not the case, since the computer science refers to mathematics in many points like the proof of statements and algorithms which is the most important thing a computer scientist must know. It is unnecessary to offer a computer science course with more mathematics than computer science. It is no wonder that so many students fail in courses of computer science, which are really close to mathematics, since mathematics lectures have no reference to computer science',
    129: 'only the argument, which is already mentioned above, was repeated. Many students are helped by going through the tasks again and again, so they can remember them better to prepare for the exams. As already stated above, there should be a discussion of the tasks at the end, as in many exercises, in order to avoid misunderstandings',
    130: 'a suitability test for the understanding of programming languages ​​would be appropriate. Most students do not drop out because they do not have previous knowledge of computer science, which is all too difficult for them, but because they can not understand it. A simple prior test that filters people out who really only study computer science because they like video games but have no understanding of the subject',
    131: 'one takes valuable time from the students by this',
    132: 'the proportion of points required to pass exams only depends on the requirements imposed on the students',
    133: 'by this, the "students\' quality" in higher semesters can be ensured',
    134: 'a simple aptitude test would filter out only a small part of the potential study dropouts. But this requires a lot of effort, because these tests must be corrected by all interested parties',
    135: 'students who are unable to pass the aptitude test, can enroll in another subject and can study computer science as a minor. In the end, they will also be in computer science lectures and exercises',
    136: 'the courses have always been there only for the knowledge transfer',
    137: 'this does not apply to the sample schedule for the (critical) start of the study',
    138: 'basic tutorials should be offered for the base lectures, where students can ask questions about the lecture material',
    139: 'which is a better preparation for independent solving of the exercises than the presentation of the almost identical tasks as on the exercise sheet',
    140: 'by this, learning matters that are not covered in the exercises can be better understood',
    141: 'by this, the courses are not used to filter out students',
    142: 'the contents of the mathematics lectures have completely been aligned with the requirements and the study goals of mathematics students. Computer scientists are partly overwhelmed with the content',
    143: 'all lectures should be recorded and put online',
    145: 'this would solve the problem with the overcrowded auditoriums',
    147: 'a more flexible study for students with children, long-distance students, students who have to work alongside, handicapped students, etc., would be possible',
    149: 'the technical prerequisites for this are already available, but so far only used in a few courses',
    152: 'the learning matter is irrelevant to the rest of the studies and the later professional activity of computer scientists',
    153: 'so we have more time for the actual computer science subjects',
    154: 'pass marks should always be absolute',
    155: 'the mathematics lectures are completely overcrowded',
    156: 'good exercises are lackware',
    157: 'in 2 years, I never had any preparation for the next sheet in any exercise, contrary to linguistics where this is standard',
    158: 'the bottleneck are personnel resources rather than the lack of space',
    159: 'there should be significantly more places to learn. Often the available places are crowded or in very noisy places (for example: in the hallways near the cafeteria)',
    160: 'this way, you can use the time between lectures and exercises more meaningfully and productively',
    161: 'this way, you can use the time between lectures and exercises more meaningfully and productively',
    162: 'thereby procrastination is encouraged during the acquisition of the lecture material',
    163: 'procrastination is a problem that every student has to tackle herself, but the university is not responsible for this. Among other things, this is part of the teaching process',
    164: 'the absolute pass marks are also fulfilled then',
    165: 'by this, learning groups can be formed and the contents of the courses can be discussed',
    166: 'by this, a wider range of courses can be created',
    167: 'if less time is needed, you will get the opportunity to discuss the solutions of the last week and there will be more time to ask and answer questions',
    168: 'if less time is needed, you will get the opportunity to discuss the solutions of the last week and there will be more time to ask and answer questions',
    169: 'then students, who are not ready to study in the field of computer science, can not start the studies',
    170: 'there are currently only a few places at the university that are suitable for the requirements of the computer science studies (computer rooms, sufficient power outlets)',
    171: 'the exercises should prepare better for the next sheet and not just introduce the solutions of the old sheet',
    172: 'the proportion of points required to pass exams should only depend on the requirements imposed on the students',
    173: 'one can achieve a good secondary school certificate also with (many) tutoring lessons, which depends on the parents\' financial situation',
    174: 'basic tutorials should be offered for the base lectures, where students can ask questions about the lecture material',
    175: 'especially the elective subjects and main modules are overlapping with math lectures. The professors should have coordinated this ',
    176: 'especially the elective subjects and main modules are overlapping with math lectures. The professors should have coordinated this ',
    177: 'The courses covering the fundamentals should be based on the same script, if they are held by different lecturers in different years',
    178: 'repeaters, who are only allowed to passively participate in the exercises due to capacity reasons, have the same chances as the other students',
    179: 'lecturers of subsequent courses then can rely on their students to master certain basic principles',
    180: 'constructive group work is desired by the lecturers',
    181: 'the talent of students often only shows after the first semesters',
    182: 'the secondary school final grades etc. are not decisive for the skills in computer science',
    183: 'studying not only imparts knowledge, but also key competencies, which may be important in other disciplines',
    184: 'thereby rework of the lecture material is encouraged',
    185: 'both mathematics and computer science students have the same previous knowledge from school for mathematics lectures',
    186: 'students, who do not fit into the room due to limited space, are denied the possibility to participate in the lectures (questions, discussions, etc.). The lack of space should be solved differently',
    187: 'some courses for the Master\'s degree course are offered with online lectures for independent learning, along with standard exercises',
    188: 'more events with reduced effort are created',
    189: 'thereby independent acquisition of new knowledge is encouraged',
    190: 'this form of events is suitable only for a part of the students',
    191: 'only the start of a study can really shows whether one can make the study',
    192: 'to some extend, the students already need more time than given to understand the material, especially in the mathematical subjects',
    193: 'a small group of students should be assigned to a tutor with whom they can regularly arrange to ask questions',
    194: 'if there is someone, who knows the strengths and weaknesses of the individual students and who has learned the learning matter him-/herself recently, he/she can additionally explain it in another way',
    195: 'each student should visit a compulsory tutorial at the beginning of their studies to get to know how to deal with their studies best',
    196: 'by this, the dropout rate can be reduced',
    197: 'lecture notes should be put online before the lecture so that students can prepare themselves',
    198: 'the lecture can be understood more easily',
    199: 'all slides should be uploaded centrally to an online portal (Ilias)',
    200: 'by this, one has the possibility to write in the forum in the mathematical subjects',
    201: 'it would be easier for the students',
    202: 'mathematical scripts should also contain proofs',
    203: 'proofs are often the most difficult part',
    204: 'then the students have no more incentive to attend the lecture',
    205: 'there are no universally applicable tips',
    206: 'there are many books, tutorials, tasks with solutions etc. online and in the library. You just have to bring enough enthusiasm for your subject to deal with',
    207: 'academics are not educated by teaching them how to calculate certain types of tasks',
    208: 'propositions are proven in the lectures',
    209: 'the proportion of points required to pass exams should only depend on the requirements imposed on the students',
    210: 'there should be significantly more places to learn. Often the available places are crowded or in very noisy places (for example: near the cafeteria)',
    211: 'theoretical computer science courses, such as "machine learning", require precisely the knowledge conveyed in mathematical courses',
    212: 'as long as one is able to study computer science as a secondary subject of an admission-free subject, a suitability test will not be able to prevent anyone from visiting the computer science courses',
    213: 'the secondary school degree only reflects a part of the abilities that a person has. Very good marks do not guarantee that you can master a medicine study. There are also candidates with a moderate school degree who would master a psychological study with very good marks',
    214: 'students, who are not interested in the lecture, do not visit them anyway. You have to discipline yourself in your studies; If you want to visit the lecture, you can do it - even if the slides are online. This way, others can already print them out and take notes in the lecture',
    215: 'I repeatingly had overlaps among theoretical as well as practical courses during the last three semesters',
    216: 'the exercises usually do not require the full 90 minutes and therefore there is enough time to ask questions',
    217: 'the exercises usually do not need the full 90 minutes and thus there is enough time to answer questions',
    218: 'there are hardly any seminar modules in the bachelor degree course',
    219: 'there should be more seminars that could also be graded',
    220: 'so you can practice for the bachelor\'s thesis as well as for giving talks',
    221: 'the allocation of CP sometimes does not correspond with the workload',
    222: 'the allocation of CP sometimes does not correspond with the workload',
    223: 'I myself have experienced that, for example, an elaboration worth 2.5 points required much more effort. An increase of the CP for these cases would be very reasonable',
    224: 'which would complicate the combination of subjects for bachelor students of two degrees ',
    225: 'it would be helpful for students to get an assessment at the beginning. You could design the aptitude test such that students can still start the study',
    226: 'usually the 90 minutes for the exercises will not suffice, if one is concerned with the student questions about the exercises or alternative ways of solution',
    227: 'this construct will not be found later in the profession of an academician (m/f). Depending on your work later, you will be the only expert in your field and/or work in a team. Therefore, learning groups are better during the study',
    228: 'misunderstandings between students and lecturers can be avoided directly at the beginning',
    229: 'some of the universal tips are about copying, plagiarism, literature research etc.',
    230: 'doctoral students also have a similar compulsory "tutorial"',
    231: 'some subjects are not covered by the exercise tasks and thus are not discussed in the exercises',
    232: 'further subjects shall be restructured. Most problems arise in the mathematical subjects, in this case it would make sense to offer specific lectures for computer scienctists',
    233: 'exercises should prepare for the next sheet and not just introduce the solutions of the old sheet',
    235: 'also the rooms\' technical equipment counts towards the capacities',
    236: 'it does not provide sufficient resources for the number of students',
    237: 'the forum for mathematical subjects does not offer inherent advantages',
    238: 'the preparation of a seminar often means a similar effort as a lecture for the lecturers and the lecturers are currently understaffed',
    239: 'all lectures should be uploaded centrally in a portal (e.g., Ilias)',
    240: 'a study aims at mature individuals, which is why it is their own responsibility how conscientiously they pursue their studies',
    241: 'in this case the copyright and exploitation rights are difficult to clarify and defend, especially if third-party material is used',
    242: 'the computer science degree was not designed as a part-time study in general and therefore would have to be completely revised',
    243: 'uniform grading criteria for seminar papers and seminar lectures should be introduced',
    244: 'thus students take seminars more seriously',
    245: 'a seminar only makes sense if the number of participants (due to the presentation scheduling) is rather small, which is only the case in a few Bachelor\'s courses',
    246: 'a presence obligation can not legally be enforced here',
    247: 'the other event forms are not equally suitable for all students, either',
    248: 'a suitability test for the computer science studies should be introduced, since a lack of computer science in schools makes the secondary school degree irrelevant for an admission restriction',
    249: 'there should be significantly more places to learn. Often the available places are crowded or in very noisy places (for example: in the hallways near the cafeteria)',
    250: 'we are not even close to having these personnel capacities',
    251: 'during exercises questions about the current lecture material can be asked already',
    252: 'this is a normal learning group and no learning group organized by the university with tutors',
    253: 'the effort for the exercise is not worthwhile if only a handful of students register for this form of the activity',
    254: 'students are adults who should recognize their strengths and weaknesses themselves and should determine their own learning behavior. One has the possibility to ask the questions about content in the lecture and in the exercise. For other questions  one can contact the mentoring team',
    255: 'one should first examine the factors that determine the success of computer science studies',
    256: 'in the subjects which I supervised, for years the workloads have always been clearly below the 75h for 2.5CP when querying the data',
    257: 'a lecture offers more than just reading the script. You usually get more background information and have the opportunity to ask questions',
    258: 'you can make notes directly in the script during the lecture',
    259: 'this costs money and there are many dropouts. Therefore it would be more sensible and cost-effective to create a better selection process',
    260: 'there are indeed also organizational matters which can be clarified this way',
    261: 'also other lectures, where the majority of the lecture is in slides, are attended',
    262: 'it makes no sense to make such an activity compulsory, because people, who only attend because it is compulsory, just rock the boat. But I like the idea',
    263: 'it is also possible to clarify organizational questions for all and not just content based questions',
    264: 'exercises should prepare better for the next sheet and not just present the solutions of the old sheet',
    265: 'I can only speak from my personal experience of the last three years, and there always was some time left. In addition, you can always arrange an appointment with tutors to clarify questions',
    266: 'that leads to the point again, that more lecturers should be hired :)',
    267: 'the same argument applies to the classical attending of the lecture',
    268: 'a classical lecture offers more than a online lecture and thus appeals to more students',
    269: 'in general, minor subjects should not be mandatory',
    270: 'computer science is about dealing with topics, which are absolutely necessary for a computer scientist in later life, and not about other subjects',
    271: 'the "look outside the box" may be interesting and desirable for some students, but sometimes drifts far from the core of computer science',
    272: 'for these courses, not all topics of the mathematical courses are necessary, but important topics are missing for these courses',
    273: 'exercises should prepare for the next sheet and should not only present the solutions of the old sheet',
    274: 'compulsory elective modules are overlapping, although these are intended for the same semester',
    275: 'in my opinion it should not be a problem if one cites all sources properly',
    276: 'we usually have just time for discussing the prototype solutions of the last sheet in a detailed manner',
    277: 'we usually have just time for discussing the prototype solutions of the last sheet in a detailed manner',
    278: 'although this is not required',
    279: 'although this is not required',
    280: 'in my opinion attending lectures is not the primary goal but achieving the greatest possible learning effect. This allows the student to handle the slides at the right time',
    281: 'we should not make the admission restriction dependent on the secondary school degree, but on a competence check or the computer science grade from school',
    282: 'each student should be responsible for themselves. If he is not able to handle the studies, then he should visit the tutorial. Otherwise it should not be mandatory',
    283: 'this helps understanding. In general, however, math scripts should be available in electronic form so that one has the possibility to achieve a greater learning effect during the lecture',
    284: 'there is no incentive for the lecture anyway, if one can not pay attention during the lecture, because one only has to write. This also does not produce a learning effect',
    285: 'computers occasionally do not work',
    286: 'we still use technologies that are decades old. We must start to modernize the faculty of science, especially the course of studies in computer science. Especially since our faculty is the one that requires the most advanced technology',
    287: 'other faculties at the HHU, where there is also a relatively high drop-out rate, already have modern computers, technologies and buildings, although innovative subjects such as computer science are more likely to need this opportunity to guarantee an appropriate teaching',
    288: 'I define customization by the student\'s need to master learned content, rather than just aiming at passing the module. At the moment the learning effect is lessened by this',
    289: 'in my opinion there should be more possibilities. This means that one should have the possibilities, on the one hand the possibility to the study the double Bachelor, and on the other hand, choosing computer science cources instead of minor subjects',
    290: 'certain scripts contain many errors that are sometimes corrected in the lecture but the corrected script is not used for the year after. In my opinion, the content of the scripts should remain, but all scripts must improve from year to year by improving the existing errors',
    291: 'it is difficult to determine which subjects are needed precisely for the later computer science courses because the events vary from semester to semester. The mathematics lectures do not cover all the topics that are necessary for computer science lectures, but they provide a solid foundation',
    292: 'such modules have only a small capacity due to the limited number of hours (one presentation per appointment only)',
    293: 'they require advanced presentation and teaching skills, especially when the module is completed with an exam',
    294: 'the number of rooms is constant and difficult to change, while new and more staff, or also fewer staff, can be employed for each semester',
    295: 'although only a part of the learning matter is really needed, the remaining content is made optional by the low pass marks',
    296: 'the CP per module is not determined according to the workload but on the basis of the 180CP-per-programme rule, so the workload should result from the CP',
    297: 'especially freshmen do not yet dare to ask questions and the lecturer often has to come up with questions himself in tutorials',
    298: 'the students are more interested in being able to solve the exercise problems well, than understanding non-exame-relevant learning matter. The interest is correspondingly low',
    299: 'the understanding of a task scheme can help to understand the background of a complex subject',
    300: 'especially freshmen have to acquire this maturity yet',
    301: 'this maturity was abolished during school',
    302: 'to me it seems more reasonable to set the 100% mark according to the best exams (for example, the average of the five best), than according to the often unrealistic expectations of the lecturer',
    303: 'the exam can not be repeated and on the basis of the pass mark only the particularly bad students will repeat a module',
    304: 'this way, an (absolutely) error-free script could be worked out',
    305: 'such exercises should not be graded',
    306: 'one module is assigned to a different number of CP depending on the course of studies, for example the Analysis 1 is worth 8 CP for physicists, 9 CP for mathematicians and 10 CP for computer scientists',
    307: 'the university educates academics and no IT specialists',
    308: 'the stimuli from other subjects can be very helpful for the way of thinking',
    309: 'you have to visit a lot of pages each day to keep up',
    310: 'there is a great risk of confusion between modules, whether the materials are in ILIAS, the student portal, their own website ore are not made available at all',
    311: 'they can help in the selection of a specialization subject, which can also be in the minor subjects',
    312: 'they offer a selectable alternative to the compulsory modules in the first semesters and thus also serve as a guide to whether the subject is the right',
    313: 'the secondary subjects should be related to computer science (according to the examination regulations) and, for many they may be part of a later profession',
    314: 'the lecturers will otherwise have no or less audience in the lectures who can give feedback',
    315: 'this is possible with ordinary lecture notes and notices, too, provided that the slides are made available, i.e., there is sufficient time for writing',
    316: 'no tutors have to be bound to groups. The consultation hours of student assistants or exercise leaders are often not well attended and therefore sufficient',
    317: 'it should be possible to reach at least 30 CP\'s in each semester without overlaps',
    318: 'example schedules are there to show students how their studies might look like. If students find this to be good and stick to it or orientate on it, there should be no difficulties. In my current semester, almost 6 elective courses are overlapping. I would have liked to attend four of them and think that this is completely irresponsible against the students and also the reputation of the university takes considerable damage.',
    319: 'also the technical equipment of the rooms counts to the capacities and does not provide sufficient resources for the number of students',
    320: 'the students often do not have the opportunity to gain the skills needed in the aptitude tests and the acquiring of such skills should be the goal of university study ',
    321: 'freshmen are not fully accustomed to university and thus a suitability can not be determined',
    322: 'we are currently provided two lectures and one of those could be used to only teach computer scientists, since we are the second biggest degree programm and have a majority in the lectures',
    323: 'the mathematics lectures are already adjusted for computer science students by requiring softer admission criteria and by passing the course without a grade',
}


def sanity_check():
    s_uids = [s.uid for s in session.query(Statement).filter_by(issue_uid=old_issue_uid).all()]
    db_textversions = session.query(TextVersion).filter(TextVersion.statement_uid.in_(s_uids)).all()
    for tv in db_textversions:
        if tv.uid not in data:
            print('Error: no translation for statement {}'.format(tv.uid))


def add_issue():
    title = 'Improve the Course of Computer-Science Studies'
    info = 'How can the studies of computer-science be improved and the problems caused by the large number of students be solved?'
    long_info = 'The number of students in computer science has increased considerably in recent years.There are numerous problems, e.g.space shortage, overcrowded lectures and a lack of places to learn: How can the studies of computer-science be improved and the problems caused by the large number of students be solved?'
    session.add(Issue(
        title=title,
        info=info,
        long_info=long_info,
        author_uid=2,
        lang_uid=1
    ))
    session.flush()
    transaction.commit()
    global new_issue_uid
    new_issue_uid = session.query(Issue).order_by(Issue.uid.desc()).first().uid
    print('Add new discussion with uid {}'.format(new_issue_uid))


def add_statements():
    statements = session.query(Statement).filter_by(issue_uid=old_issue_uid).all()

    pkey = session.query(Statement).order_by(Statement.uid.desc()).first().uid
    for statement in statements:
        print('Adding statement textversion {}, is_position {}, issue {}, is_disabled {}'.format(1, statement.is_startpoint, new_issue_uid, statement.is_disabled))
        s = Statement(
            textversion=1,
            is_position=statement.is_startpoint,
            issue=new_issue_uid,
            is_disabled=statement.is_disabled
        )
        session.add(s)
        pkey += 1
        s.uid = pkey
        session.flush()
        transaction.commit()
        statement_from_old_to_new[statement.uid] = session.query(Statement).order_by(Statement.uid.desc()).first().uid
        statement_from_new_to_old[session.query(Statement).order_by(Statement.uid.desc()).first().uid] = statement.uid


def add_textversions():
    s_uids = [s.uid for s in session.query(Statement).filter_by(issue_uid=old_issue_uid).all()]
    db_textversions = session.query(TextVersion).filter(TextVersion.statement_uid.in_(s_uids)).all()
    pkey = session.query(TextVersion).order_by(TextVersion.uid.desc()).first().uid

    for tv in db_textversions:
        print('Adding TextVersion content "{}", author {}, statement_uid {}, is_disabled {}'.format(data[tv.uid][:10], tv.author_uid, statement_from_old_to_new[tv.statement_uid], tv.is_disabled))
        tv = TextVersion(
            content=data[tv.uid],
            author=tv.author_uid,
            statement_uid=statement_from_old_to_new[tv.statement_uid],
            is_disabled=tv.is_disabled
        )
        pkey += 1
        tv.uid = pkey
        session.add(tv)

    session.flush()
    transaction.commit()


def set_textversion_to_statements():
    statements = session.query(Statement).filter_by(issue_uid=new_issue_uid).all()

    for s in statements:
        uid = session.query(TextVersion).filter_by(statement_uid=s.uid).order_by(TextVersion.uid.desc()).first().uid
        print('Reassign TextVersion {} to statement {}'.format(s.uid, uid))
        s.set_textversion(uid)

    session.flush()
    transaction.commit()


def add_premisegroups():
    premises = session.query(Premise).filter_by(issue_uid=old_issue_uid).all()
    pkey = session.query(PremiseGroup).order_by(PremiseGroup.uid.desc()).first().uid
    pgroup_ids = list(set([premise.premisesgroup_uid for premise in premises]))
    for pgroup_id in pgroup_ids:
        tmp = session.query(PremiseGroup).filter_by(uid=pgroup_id).first()
        print('Adding PremiseGroup author {}'.format(tmp.author_uid))
        pg = PremiseGroup(author=tmp.author_uid)
        session.add(pg)
        pkey += 1
        pg.uid = pkey
        session.flush()
        transaction.commit()
        pgroups_from_old_to_new[pgroup_id] = pkey


def add_premises():
    premises = session.query(Premise).filter_by(issue_uid=old_issue_uid).all()
    pkey = session.query(Premise).order_by(Premise.uid.desc()).first().uid

    for premise in premises:
        print('Adding Premise premisesgroup {}, statement {}, is_negated {}, author {}, issue {}, is_disabled'.format(
            pgroups_from_old_to_new[premise.premisesgroup_uid], statement_from_old_to_new[premise.statement_uid], premise.is_negated,
            premise.author_uid, premise.issue_uid, premise.is_disabled))
        p = Premise(
            premisesgroup=pgroups_from_old_to_new[premise.premisesgroup_uid],
            statement=statement_from_old_to_new[premise.statement_uid],
            is_negated=premise.is_negated,
            author=premise.author_uid,
            issue=premise.issue_uid,
            is_disabled=premise.is_disabled
        )
        pkey += 1
        p.uid = pkey
        session.add(p)
    session.flush()
    transaction.commit()


def add_arguments():
    arguments = session.query(Argument).filter_by(issue_uid=old_issue_uid).all()
    pkey = session.query(Argument).order_by(Argument.uid.desc()).first().uid
    argument_from_old_to_new = {}

    new_order = {argument.uid: argument for argument in arguments}
    arguments = collections.OrderedDict(sorted(new_order.items()))

    for key, argument in arguments.items():
        pkey += 1
        a = pgroups_from_old_to_new[argument.premisesgroup_uid]
        b = statement_from_old_to_new[argument.conclusion_uid] if argument.conclusion_uid else None
        c = argument_from_old_to_new[argument.argument_uid] if argument.argument_uid else None
        print(
            'Adding Argument ({} -> {}) premisegroup {}, conclusion {}, argument {}, issupportive {}, author {}, issue {}, is_disabled {}'.format(
                argument.uid, pkey, a, b, c, argument.is_supportive, argument.author_uid, new_issue_uid, argument.is_disabled))
        a = Argument(
            premisegroup=a,
            conclusion=b,
            argument=c,
            issupportive=argument.is_supportive,
            author=argument.author_uid,
            issue=new_issue_uid,
            is_disabled=argument.is_disabled
        )
        a.uid = pkey
        session.add(a)
        session.flush()
        transaction.commit()
        uid = session.query(Argument).order_by(Argument.uid.desc()).first().uid
        argument_from_old_to_new[argument.uid] = uid


if __name__ == "__main__":
    sanity_check()
    add_issue()
    if new_issue_uid == 0:
        exit(1)
    add_statements()
    add_textversions()
    set_textversion_to_statements()
    add_premisegroups()
    add_premises()
    add_arguments()
