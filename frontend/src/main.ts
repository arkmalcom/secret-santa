const form = document.getElementById('santa-form') as HTMLFormElement;
const participantsContainer = document.getElementById('participants-container')!;
const addParticipantButton = document.getElementById('add-participant')!;

let participantCount = 1;

addParticipantButton.addEventListener('click', () => {
  participantCount++;
  const participantDiv = document.createElement('div');
  participantDiv.classList.add('participant', 'mb-4');
  participantDiv.innerHTML = `
    <label for="participant-${participantCount}" class="block text-sm font-medium text-gray-700">
      Participante ${participantCount}
    </label>
    <input
      type="text"
      id="participant-${participantCount}"
      name="participant-${participantCount}"
      class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      placeholder="Nombre"
      required
    />
  `;
  participantsContainer.appendChild(participantDiv);
});

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const participants: string[] = [];

  formData.forEach((value, key) => {
    participants.push(value.toString());
  });

  console.log('Participants:', participants);

  // TODO: Replace console.log with an API call to send data to the backend
  // fetch('/api/secret-santa', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ participants }),
  // });
});
