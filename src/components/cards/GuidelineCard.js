import Image from "next/image";

const GuidelineCard = ({ title, text, link }) => {

  return (
    <a
      href={link}
      className="max-w-[280px] hover:shadow-xl transform hover:scale-105 transition duration-300 mx-2"
    > 
      <div className="h-[100px] relative">
        <Image 
          className="object-cover"
          src="/base_guideline.webp" 
          alt="Card Image" 
          fill
          sizes="180px"
        />
      </div>

      <div className="px-4 py-3">
        <div className="font-bold text-xl mb-2">{title}</div>
        <p className="text-gray-700 text-base">
          {text}
        </p>
      </div>
    </a>
  );
};

export { GuidelineCard };
