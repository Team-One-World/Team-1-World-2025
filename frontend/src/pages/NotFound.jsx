import { Link } from "react-router-dom";

function NotFound() {
    return (
      <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white">
        <h1 className="text-9xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600 mb-8 typewriter">404</h1>
        <p className="text-2xl font-medium text-gray-400 mb-8 typewriter">
          The page you're looking for doesn't exist.
        </p>
        <Link
          to="/"
          className="btn-primary"
        >
          Go Home
        </Link>
      </div>
    );
}

export default NotFound;