import { PrimaryButton, SecondaryButton, ThirdButton, ForthButton } from "@/components/buttons";

export default function UiResources() {
  return (
    <div className="min-h-full">
      <h1 className="text-4xl font-bold text-center">UI Resources</h1>

      <div className="flex flex-col items-center justify-center">
        <h2> UI Resources </h2>
        <PrimaryButton text="Primary Button" />
        <SecondaryButton text="Secondary Button" />
        <ThirdButton text="Third Button" />
        <ForthButton text="Forth Button" />
      </div>
    </div>
  )
}