const SecondaryButton = ({ text }) => {
  return (
    <button className="bg-secondary hover:bg-secondary/80 text-white font-bold py-2 px-4 rounded">
      {text}
    </button>
  )
}

export {
  SecondaryButton
}
