import React, { useState } from "react";
import { useParams } from "react-router-dom";

function Pair() {
  const { listId } = useParams();
  const [phoneNumber, setPhoneNumber] = useState("");
  const [pairName, setPairName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const BASE_API_URL =
    "https://u9snk0ziib.execute-api.us-east-2.amazonaws.com/api";

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    let pairedUser = "";

    try {
      const userResponse = await fetch(
        `${BASE_API_URL}/users/${listId}/${phoneNumber}`,
        {
          method: "GET",
        },
      );

      if (!userResponse.ok) {
        throw new Error("Este usario no existe en esta lista.");
      }

      const data = await userResponse.json();
      const userPublicId = data.user_public_id;

      const pairResponse = await fetch(
        `${BASE_API_URL}/pairings/${listId}/${userPublicId}`,
        {
          method: "GET",
        },
      );

      if (pairResponse.status === 404) {
        const pairCreateResponse = await fetch(
          `${BASE_API_URL}/pairings/create/${listId}/${userPublicId}`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
          },
        );
        if (!pairCreateResponse.ok) {
          throw new Error("Error al crear un nuevo emparejamiento");
        }

        const pairCreateData = await pairCreateResponse.json();
        pairedUser = pairCreateData.receiving_user_name;
      } else if (!pairResponse.ok) {
        throw new Error("Error al obtener el emparejamiento");
      } else {
        throw new Error("Tu angelito ya ha sido asignado.");
      }
    } catch (err: any) {
      setError(err.message || "Ocurrió un error");
    } finally {
      setPairName(pairedUser);
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-green-600 flex items-center justify-center text-center text-white flex-col space-y-4">
      {pairName ? (
        <div className="flex justify-center text-center items-center bg-green-800 border-2 border-red-600 flex-col space-y-2 p-6">
          <h1 className="text-2xl font-bold">¡Tu angelito está listo!</h1>
          <p className="text-xl mt-2">
            El nombre de tu angelito es:{" "}
            <span className="text-red-500 font-semibold">{pairName}</span>
          </p>
          <p>
            Por favor escribe el nombre o toma una captura de pantalla para no
            olvidarlo.
          </p>
          <p>
            Para mantener el angelito secreto, no podras acceder a esta pagina
            nuevamente.
          </p>
        </div>
      ) : (
        <div className="w-full max-w-md bg-white rounded shadow-md p-6">
          <h1 className="text-2xl font-bold mb-4 text-center text-black">
            Ingresa tu número de teléfono
          </h1>
          {error && <p className="text-red-500">{error}</p>}
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="tel"
              className="w-full p-2 border border-gray-300 rounded-md shadow-sm text-black focus:ring-blue-500 focus:border-blue-500"
              placeholder="Número de teléfono"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              required
            />
            <button
              type="submit"
              className="w-full bg-green-800 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:ring focus:ring-blue-300"
              disabled={loading}
            >
              {loading ? "Buscando tu angelito..." : "Buscar mi angelito"}
            </button>
          </form>
        </div>
      )}
    </div>
  );
}

export default Pair;
