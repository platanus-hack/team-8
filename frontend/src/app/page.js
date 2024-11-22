import { PrimaryButton, SecondaryButton, ThirdButton, ForthButton } from "@/components/buttons";


export default function Home() {
  return (
    <div className="min-h-full">
      <h1 className="text-4xl font-bold text-center">Welcome to ACSED</h1>

      <PrimaryButton text="Primary Button" />
      <SecondaryButton text="Secondary Button" />
      <ThirdButton text="Third Button" />
      <ForthButton text="Forth Button" />
    </div>
  );
}
