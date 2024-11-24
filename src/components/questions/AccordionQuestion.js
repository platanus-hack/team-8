// components/QuestionAccordion.js

import React, { useState } from 'react';

const QuestionAccordion = ({ questionData }) => {
  const [isOpen, setIsOpen] = useState(false);

  const {
    questionNumber,
    questionType,
    question,
    guidelineAnswer,
    studentAnswer,
    score,
    alternatives,
    studentJustification,
    guidelineJustification,
  } = questionData;

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
    <div className="mb-4 border border-gray-200 rounded">
      {/* Accordion Header */}
      <button
        className="w-full text-left bg-gray-100 px-4 py-2 font-semibold flex justify-between items-center"
        onClick={() => setIsOpen(!isOpen)}
      >
        <span>
          Question {questionNumber} - {questionType}
        </span>
        <span>Score: {score}</span>
      </button>

      {/* Accordion Content */}
      {isOpen && (
        <div className="bg-white p-4">
          {/* Include the same content as the Question Detail Card here */}
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
      )}
    </div>
  );
};

export { QuestionAccordion };
