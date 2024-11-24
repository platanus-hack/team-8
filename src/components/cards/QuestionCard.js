import React from 'react';

const QuestionCard = ({
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
        return 'bg-gray-500';
    }
  };


  console.log('studentScore:', studentScore);

  return (
    <div className="bg-white border border-gray-200 shadow-md rounded-md p-6 space-y-6 w-[600px] mx-auto">
      {/* Div 1 */}
      <div className="flex pb-6 border-b border-gray-200">
        {/* Left Div (1/3) */}
        <div className="w-1/3 pr-4 flex flex-col space-y-2 border-r border-gray-200 mr-3">
          {/* Question Number */}
          <div>
            <span className="text-gray-600">N° de pregunta:</span>{' '}
            <span className="font-semibold">{questionNumber}</span>
          </div>
          {/* Score */}
          <div>
            <span className="text-gray-600">Puntaje:</span>{' '}
            <span className="font-semibold">{studentScore}</span>
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
        {/* Right Div (2/3) */}
      </div>

      {/* Div 2: Expected Answer */}
      <div className="pb-6 border-b border-gray-200">
        <h3 className="text-lg font-semibold mb-2">Respuesta esperada</h3>
        <p className="text-gray-800">{guidelineAnswer}</p>
      </div>
    </div>
  );
};

export { QuestionCard };
