function NotFound() {
    return (
      <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
        <h1 className="text-9xl   
   font-bold text-gray-800 mb-8 typewriter">404</h1>
        <p className="text-2xl font-medium text-gray-600 mb-8 typewriter">
          The page you're looking for doesn't exist.
        </p>
        <a
          href="/"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Go Home
        </a>
      </div>
    );
}
  
  
  export default NotFound;