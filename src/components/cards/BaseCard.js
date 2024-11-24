import Image from "next/image";
import { SecondaryButton } from "../buttons";

const BaseCard = ({ title, text, image, link, isClickable, hasImage, buttonText }) => {
  const Wrapper = isClickable ? 'a' : 'div';
  const cardClasses = `w-[320px] h-[400px] rounded overflow-hidden shadow-lg ${
    isClickable ? 'hover:shadow-xl transform hover:scale-105 transition duration-300' : ''
  }`;

  return (
    <Wrapper
      href={isClickable ? link : undefined}
      className={cardClasses}
    > 
      {/* Image has passed as a prop */}
      {hasImage && image && (
        <div className="h-[200px] relative">
        <Image 
          className="object-cover"
          src={image} 
          alt="Card Image" 
          fill
          sizes="320px"
        />
      </div>
      )}

      {/* Set default image if not passed as a prop */}
      {!hasImage && (
        <div className="h-[200px] relative">
          <Image 
          className="object-cover"
          src="/logo.jpeg" 
          alt="Card Image" 
          fill
          sizes="320px"
        />
        </div>
      )}

      <div className="px-4 py-3">
        <div className="font-bold text-xl mb-2">{title}</div>
        <p className="text-gray-700 text-base">
          {text}
        </p>
      </div>
      {!isClickable && (
        <div className="px-4 py-3">
          <SecondaryButton text={buttonText} />
        </div>
      )}
    </Wrapper>
  );
};

export { BaseCard };
