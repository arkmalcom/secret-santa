import { useParams } from 'react-router-dom';

function List() {
  const { listId } = useParams();

  return (
    <div className="min-h-screen bg-green-600 flex items-center justify-center text-center text-red-400 text-xl flex-col space-y-2">
      <h1>¡Lista creada con éxito!</h1>
      <p>Aqui esta el link para compartir:</p>
      <a href='https://angelito.com/pair/{listId}' className="text-blue-300">https://angelito.com/pair/{listId}</a>
    </div>
  );
}

export default List;
