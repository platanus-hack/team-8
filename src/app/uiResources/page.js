'use client';
import { PrimaryButton, SecondaryButton, ThirdButton, ForthButton } from "@/components/buttons";
import { BaseCard, UltimateCard } from "@/components/cards";
import { QuestionAccordion, QuestionDetailCard } from '@/components/questions';

export default function UiResources() {
  const cardsTypes = [
    {
      title: "Carta Base",
      text: "Esta es una carta base para poder crear cartas más personalizadas",
      image: "/logo.jpeg",
      link: "https://www.google.com",
      isClickable: true,
      hasImage: true,
      buttonText: "Ver más"
    },
    {
      title: "Carta tipo 1",
      text: "Es una carta con IMAGEN, CLICKABLE Y HOVERLABLE, sin botón de acción",
      image: "/logo.jpeg",
      link: "https://www.google.com",
      isClickable: true,
      hasImage: true,
      buttonText: "Ver más"
    },
    {
      title: "Carta tipo 2",
      text: "Es una carta con IMAGEN, NO CLICKABLE Y NO HOVERABLE, con un botón de acción",
      image: "/logo.jpeg",
      link: "https://www.google.com",
      isClickable: false,
      hasImage: true,
      buttonText: "Ver más"
    },
    {
      title: "Carta tipo 4",
      text: "Es una carta sin IMAGEN, CLICKABLE Y HOVERABLE, sin botón de acción",
      image: "",
      link: "https://www.google.com",
      isClickable: true,
      hasImage: false,
      buttonText: "Ver más"
    },
    {
      title: "Carta tipo 3",
      text: "Es una carta sin IMAGEN, NO CLICKABLE Y NO HOVERABLE, con un botón de acción",
      image: "",
      link: "https://www.google.com",
      isClickable: false,
      hasImage: false,
      buttonText: "Ver más"
    }
  ]

  const questionMockData = {
    id: 1,
    questionNumber: 1,
    question: "¿Cuál es tu comida favorita?",
    questionType: "development",
    guidelineAnswer: "Pizza",
    studentAnswer: "Pizza",
    score: 10,
    alternatives: null,
    studentJustification: null,
    guidelineJustification: null,
  }

  const ultimateCardMockData = {
    questionNumber: 1,  
    questionType: "development",
    question: "¿Cuál es tu comida favorita?",
    guidelineAnswer: "Pizza",
    studentAnswer: "Hamburguesa",
    studentScore: 4.6, // 0 - 10
    modelFeedback: "Pizza",
  }

  return (
    <div className="min-h-full">
      <h1 className="text-4xl font-bold text-center">UI Resources</h1>

      <h2 className="text-2xl font-bold text-center"> Buttons </h2>
      <div className="flex flex-col items-center justify-center gap-2 my-5">
        <PrimaryButton text="Primary Button" />
        <SecondaryButton text="Secondary Button" />
        <ThirdButton text="Third Button" />
        <ForthButton text="Forth Button" />
      </div>

      <h2 className="text-2xl font-bold text-center"> Cards </h2>
      <div className="flex flex-row items-center justify-center flex-wrap gap-2 my-5">
        {cardsTypes.map((card, index) => (
          <BaseCard key={index} {...card} />
        ))}
      </div>

      <h2 className="text-2xl font-bold text-center"> Bolt Components </h2>
      <div className="flex flex-col items-center justify-center gap-2 my-5">
        <QuestionAccordion questionData={questionMockData} />
        <QuestionDetailCard {...questionMockData} />
        <UltimateCard {...ultimateCardMockData} />
      </div>
    </div>
  )
}