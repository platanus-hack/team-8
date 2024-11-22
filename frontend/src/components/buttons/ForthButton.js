const ForthButton = ({ text }) => {
  return (
    <button className="bg-forth hover:bg-forth/80 text-white font-bold py-2 px-4 rounded">
      {text}
    </button>
  )
}

export {
  ForthButton
}
