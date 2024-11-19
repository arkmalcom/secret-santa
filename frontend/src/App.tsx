import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './style.css';

function App() {
  const [participants, setParticipants] = useState([{ id: 1, name: '', phone_number: '' }]);
  const BASE_API_URL = "https://u9snk0ziib.execute-api.us-east-2.amazonaws.com/api"
  const navigate = useNavigate();

  function addParticipant() {
    setParticipants([...participants, { id: participants.length + 1, name: '', phone_number: '' }]);
  }

  function handleChange(id: number, field: 'name' | 'phone_number', value: string) {
    setParticipants(participants.map(p => 
      p.id === id ? { ...p, [field]: value } : p
    ));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const users = participants.map(participant => ({
      name: participant.name,
      phone_number: participant.phone_number,
    }));

    try {
      const response = await fetch(`${BASE_API_URL}/lists/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({ users }),
      });

      if (!response.ok) {
        throw new Error('Error al crear la lista');
      }

      const data = await response.json();
      const listId = data.list_id;

      navigate(`/list/${listId}`);
    } catch (error) {
      console.error('Error:', error);
      alert('Hubo un problema al enviar el formulario.');
    }
  }

  return (
    <div className="min-h-screen bg-green-600 flex items-center justify-center">
      <div className="w-full max-w-md bg-white rounded shadow-md p-6">
        <h1 className="text-2xl font-bold mb-4 text-center">Angelito</h1>
        <form id="santa-form" onSubmit={handleSubmit}>
          <div id="participants-container" className="space-y-4">
            {participants.map(participant => (
              <div key={participant.id} className="participant">
                <label
                  htmlFor={`participant-${participant.id}`}
                  className="block text-sm font-medium text-gray-700"
                >
                  Participante {participant.id}
                </label>
                <input
                  type="text"
                  id={`participant-name-${participant.id}`}
                  name={`participant-name-${participant.id}`}
                  value={participant.name}
                  onChange={e => handleChange(participant.id, 'name', e.target.value)}
                  className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Nombre"
                  required
                />
                <input
                  type="tel"
                  id={`participant-phone-${participant.id}`}
                  name={`participant-phone-${participant.id}`}
                  value={participant.phone_number}
                  onChange={e => handleChange(participant.id, 'phone_number', e.target.value)}
                  className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Teléfono"
                  required
                />
              </div>
            ))}
          </div>
          <button
            id="add-participant"
            type="button"
            onClick={addParticipant}
            className="w-full bg-red-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:ring focus:ring-red-800 mt-4"
          >
            Agregar Participante
          </button>
          <button
            type="submit"
            className="w-full bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 mt-4 focus:ring focus:ring-green-300"
          >
            Enviar
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
