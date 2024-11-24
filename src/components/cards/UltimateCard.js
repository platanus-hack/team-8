import React from 'react';
import { CircularProgressbar } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const UltimateCard = ({
  questionNumber,
  questionType,
  question,
  guidelineAnswer,
  studentAnswer,
  studentScore,
  modelFeedback,
}) => {
  // Function to determine badge color based on question type
  const getBadgeColor = (type) => {
    switch (type) {
      case 'multipleChoice':
        return 'bg-blue-500';
      case 'trueOrFalse':
        return 'bg-green-500';
      case 'short answer':
        return 'bg-yellow-500';
      case 'development':
        return 'bg-purple-500';
      default:
        return 'bg-purple-500';
    }
  };

  return (
    <div className="bg-white border border-gray-200 shadow-md rounded-md p-6 space-y-6 w-[600px] mx-auto">
      {/* Div 1 */}
      <div className="flex pb-6 border-b border-gray-200">


        {/* Left Div (2/3) */}
        <div className="w-2/3 pr-4 flex flex-col space-y-2 border-r border-gray-200 mr-3 gap-4">

          <div className="flex flex-row justify-center gap-4">
            {/* Question Number */}
            <div>
              <span className="text-black font-semibold">N° de pregunta:</span>{' '}
              <span className="font-semibold">{questionNumber}</span>
            </div>

            {/* Question Type Badge */}
            <div>
              <span
                className={`inline-block px-2 py-1 text-sm font-semibold text-white rounded-full ${getBadgeColor(
                  questionType
                )}`}
              >
                {questionType}
              </span>
            </div>
          </div>
          
          <div className="flex flex-row justify-center">
            <p className="text-black font-bold">{question}</p>
          </div>

        </div>


        {/* Right Div (1/3) */}
        <div className="w-1/3 flex items-center justify-center">
          <div className="w-24 h-24">
            <CircularProgressbar
              value={`${studentScore * 10}`}
              text={`${studentScore * 10}`}
              styles={{
                path: {
                  stroke: '#4CAF50',
                  strokeLinecap: 'round',
                },
                trail: {
                  stroke: '#e6e6e6',
                },
                text: {
                  fill: '#333',
                  fontSize: '16px',
                  fontWeight: 'bold',
                },
              }}
            />
          </div>
        </div>
     


      </div>

      {/* Div 2: Expected Answer */}
      <div className="pb-6 border-b border-gray-200">
        <h3 className="text-lg font-semibold mb-2">Respuesta esperada 🧑‍🏫</h3>
        <p className="text-gray-800">➡️ {guidelineAnswer}</p>
      </div>

      {/* Div 3: Student Answer */}
      <div className="pb-6 border-b border-gray-200">
        <h3 className="text-lg font-semibold mb-2">Respuesta alumno 🧐</h3>
        <p className="text-gray-800">➡️{studentAnswer}</p>
      </div>

      {/* Div 4: Model Feedback */}
      <div className="pb-6 border-gray-200">
        <h3 className="text-lg font-semibold mb-2">Feedback del modelo 🤖</h3>
        <p className="text-gray-800 typewriter">
          ➡️ {modelFeedback}
        </p>
      </div>
    </div>
  );
};

export { UltimateCard };
