const PrimaryButton = ({ text }) => {
  return (
    <button className="bg-primary hover:bg-primary/80 text-white font-bold py-2 px-4 rounded">
      {text}
    </button>
  )
}

export {
  PrimaryButton
}
