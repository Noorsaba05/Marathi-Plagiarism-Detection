# build_corpus.py
# Real Marathi academic corpus for demo purposes

import json
import os

def build_corpus():

    # Real Marathi academic sentences covering multiple topics
    # Sourced from Marathi Wikipedia and academic text manually
    marathi_sentences = [

        # भारत / India
        "भारत हे दक्षिण आशियातील एक प्रजासत्ताक राष्ट्र आहे.",
        "भारताची लोकसंख्या जगात दुसऱ्या क्रमांकावर आहे.",
        "भारत हा जगातील सर्वात मोठा लोकशाही देश आहे.",
        "भारताची राजधानी नवी दिल्ली आहे.",
        "भारताला १५ ऑगस्ट १९४७ रोजी स्वातंत्र्य मिळाले.",

        # महाराष्ट्र / Maharashtra
        "महाराष्ट्र हे भारताच्या पश्चिम भागात वसलेले राज्य आहे.",
        "मुंबई ही महाराष्ट्राची राजधानी आणि भारताची आर्थिक राजधानी आहे.",
        "महाराष्ट्रात मराठी ही प्रमुख भाषा बोलली जाते.",
        "महाराष्ट्र राज्याची स्थापना १ मे १९६० रोजी झाली.",
        "पुणे हे महाराष्ट्रातील एक प्रमुख शैक्षणिक केंद्र आहे.",

        # मराठी भाषा / Marathi Language
        "मराठी ही इंडो-आर्यन भाषा कुटुंबातील एक भाषा आहे.",
        "मराठी भाषेला सुमारे दोन हजार वर्षांचा इतिहास आहे.",
        "मराठी ही महाराष्ट्र राज्याची अधिकृत राजभाषा आहे.",
        "देवनागरी लिपीत मराठी भाषा लिहिली जाते.",
        "मराठी साहित्याला संत ज्ञानेश्वर आणि तुकाराम यांची मोठी देणगी आहे.",

        # शिक्षण / Education
        "शिक्षण हे मानवाच्या सर्वांगीण विकासाचे प्रमुख साधन आहे.",
        "प्राथमिक शिक्षण हे प्रत्येक मुलाचा मूलभूत अधिकार आहे.",
        "उच्च शिक्षणामुळे राष्ट्राच्या आर्थिक विकासाला गती मिळते.",
        "डिजिटल शिक्षणामुळे ग्रामीण भागातील विद्यार्थ्यांना संधी मिळत आहे.",
        "शिक्षणाशिवाय समाजाचा विकास शक्य नाही.",

        # विज्ञान / Science
        "विज्ञान आणि तंत्रज्ञान यांचा विकास राष्ट्राच्या प्रगतीसाठी आवश्यक आहे.",
        "भारताने अंतराळ संशोधनात मोठी प्रगती केली आहे.",
        "इस्रो ही भारताची प्रमुख अंतराळ संशोधन संस्था आहे.",
        "वैज्ञानिक दृष्टिकोन समाजाच्या विकासासाठी महत्त्वाचा आहे.",
        "संगणक विज्ञानाने माहिती तंत्रज्ञान क्षेत्रात क्रांती केली आहे.",

        # संविधान / Constitution
        "भारतीय संविधान हे जगातील सर्वात मोठे लिखित संविधान आहे.",
        "संविधानाने भारतातील प्रत्येक नागरिकाला समान हक्क दिले आहेत.",
        "डॉ. बाबासाहेब आंबेडकर हे भारतीय संविधानाचे शिल्पकार आहेत.",
        "भारतीय संविधान २६ जानेवारी १९५० रोजी अंमलात आले.",
        "संविधानाने भाषण स्वातंत्र्य आणि अभिव्यक्ती स्वातंत्र्य दिले आहे.",

        # पर्यावरण / Environment
        "पर्यावरण संरक्षण ही काळाची गरज आहे.",
        "जागतिक तापमानवाढ ही एक गंभीर समस्या बनत आहे.",
        "वृक्षतोड थांबवणे पर्यावरण रक्षणासाठी अत्यंत आवश्यक आहे.",
        "नैसर्गिक संसाधनांचा शाश्वत वापर करणे महत्त्वाचे आहे.",
        "प्रदूषण कमी करण्यासाठी सौर ऊर्जेचा वापर वाढवला पाहिजे.",

        # तंत्रज्ञान / Technology
        "माहिती तंत्रज्ञानाने जगाला एक जागतिक गाव बनवले आहे.",
        "कृत्रिम बुद्धिमत्ता भविष्यातील तंत्रज्ञानाचा आधारस्तंभ आहे.",
        "डिजिटल इंडिया उपक्रमाने देशाच्या डिजिटल पायाभूत सुविधा मजबूत केल्या.",
        "मोबाइल तंत्रज्ञानाने संवाद क्षेत्रात आमूलाग्र बदल घडवला आहे.",
        "सायबर सुरक्षा हे डिजिटल युगातील एक महत्त्वाचे आव्हान आहे.",
    ]

    english_sentences = [
        "India is a democratic republic with a federal structure of government",
        "Maharashtra is located in the western part of India",
        "Mumbai is the capital of Maharashtra and the financial capital of India",
        "Marathi is an Indo-Aryan language spoken predominantly in Maharashtra",
        "The Devanagari script is used to write the Marathi language",
        "Education plays a vital role in the social and economic development of a nation",
        "Primary education is a fundamental right of every child",
        "Science and technology are the driving forces of modern civilization",
        "ISRO is India's premier space research organization",
        "The Constitution of India guarantees fundamental rights to all citizens",
        "Dr. Babasaheb Ambedkar was the chief architect of the Indian Constitution",
        "Environmental conservation is essential for sustainable development",
        "Global warming is becoming a serious threat to the planet",
        "Information technology has transformed communication and commerce globally",
        "Artificial intelligence is the cornerstone of future technology",
        "Cyber security is an important challenge in the digital age",
        "India gained independence on 15th August 1947",
        "Digital India initiative has strengthened the country digital infrastructure",
        "India has made significant progress in space research",
        "Higher education accelerates the economic development of a nation",
    ]

    corpus = {
        "marathi": marathi_sentences,
        "english": english_sentences
    }
    marathi_sentences = [s.rstrip('.') for s in marathi_sentences]

    with open("corpus_data.json", "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)

    print(f"[Corpus] Saved {len(marathi_sentences)} Marathi sentences")
    print(f"[Corpus] Saved {len(english_sentences)} English sentences")
    print("[Corpus] corpus_data.json ready!")

    print("\n[Preview] Sample Marathi sentences:")
    for i, s in enumerate(marathi_sentences[:5]):
        print(f"  [{i+1}] {s}")

if __name__ == "__main__":
    build_corpus()