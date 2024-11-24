import Image from "next/image";

const LandingPage = () => {
  return (
    <div>
      <section className="bg-gray-100 border-b py-8">
        <div className="container max-w-5xl mx-auto m-6">
          <h2
            className="w-full text-5xl font-black leading-tight text-center text-gray-800 mb-5"
          >
            Tú enseña, nosotros corregimos 😉
          </h2>
          <div className="w-full mb-4">
            <div
              className="h-1 mx-auto gradient w-64 opacity-25 my-0 py-0 rounded-t"
            ></div>
          </div>

          <div className="flex flex-wrap items-center">
            {/* Div 1 */}
            <div className="w-5/6 sm:w-1/2 p-3 flex flex-col justify-center">
              <h3 className="text-3xl text-gray-800 font-bold leading-none mb-3">
                No más noches de correciones
              </h3>
              <p className="text-gray-600 mb-3">
                En cosa de minutos, te ayudamos a corregir tus pruebas, controles, tareas y mucho más.
              </p>
            </div>

            {/* Div 2 */}
            <div className="w-full sm:w-1/2 p-3">
              <Image 
                src="/happy_teacher_woman_bgremoved.png" 
                alt="Sad teacher man" 
                className="h-64 w-auto mx-auto object-contain rounded-full"
                width={650}
                height={650}
              />
            </div>
          </div>

          <div className="flex flex-wrap flex-col-reverse sm:flex-row items-center">
          <div className="w-full sm:w-1/2 p-3">
            <Image 
                src="/sad_teacher_man_bgremoved.png" 
                alt="Sad teacher man" 
                className="h-64 w-auto mx-auto object-contain rounded-full"
                width={650}
                height={650}
              />
            </div>
            <div className="w-full sm:w-1/2 p-3 flex flex-col justify-center">
              <div className="align-middle">
                <h3 className="text-3xl text-gray-800 font-bold leading-none mb-3">
                  Enfócate en lo que realmente importa, tus alumnos
                </h3>
                <p className="text-gray-600 mb-8">
                  Obtiene información sobre las fortalezas y debilidades de tus alumnos.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
export default LandingPage;