
// components/QuestionDetailCard.js

import React from 'react';

const QuestionDetailCard = ({
  questionNumber,
  questionType,
  question,
  guidelineAnswer,
  studentAnswer,
  score,
  alternatives,
  studentJustification,
  guidelineJustification,
}) => {
  // Function to determine badge color based on question type
  const getBadgeColor = (type) => {
    switch (type.toLowerCase()) {
      case 'multiple choice':
        return 'bg-blue-500';
      case 'true/false':
        return 'bg-green-500';
      case 'short answer':
        return 'bg-yellow-500';
      case 'essay':
        return 'bg-purple-500';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <div className="bg-white shadow-md rounded-md p-6 mb-6">
      {/* Header Section */}
      <div className="flex justify-between items-center mb-4">
        <div>
          <h2 className="text-xl font-bold">Question {questionNumber}</h2>
          <span
            className={`inline-block px-2 py-1 text-sm font-semibold text-white rounded-full ${getBadgeColor(
              questionType
            )}`}
          >
            {questionType}
          </span>
        </div>
        <div className="text-right">
          <span className="text-gray-600">Score:</span>{' '}
          <span className="font-semibold">{score}</span>
        </div>
      </div>

      {/* Question Text */}
      <div className="mb-4">
        <p className="text-gray-800">{question}</p>
        {/* Alternatives, if any */}
        {alternatives && alternatives.length > 0 && (
          <ul className="list-disc list-inside mt-2">
            {alternatives.map((alternative, index) => (
              <li key={index}>{alternative}</li>
            ))}
          </ul>
        )}
      </div>

      {/* Answers Section */}
      <div className="mb-4">
        <h3 className="text-lg font-semibold mb-2">Guideline Answer</h3>
        <p className="text-gray-800">{guidelineAnswer}</p>
      </div>
      <div className="mb-4">
        <h3 className="text-lg font-semibold mb-2">Student Answer</h3>
        <p className="text-gray-800">{studentAnswer}</p>
      </div>

      {/* Justifications */}
      <div className="mb-4">
        <h3 className="text-lg font-semibold mb-2">Guideline Justification</h3>
        <p className="text-gray-800">{guidelineJustification}</p>
      </div>
      <div>
        <h3 className="text-lg font-semibold mb-2">Student Justification</h3>
        <p className="text-gray-800">{studentJustification}</p>
      </div>
    </div>
  );
};

export { QuestionDetailCard };
