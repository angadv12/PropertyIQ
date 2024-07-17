import { Link } from 'react-router-dom'

const NotFoundPage = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
        <h1 className=" font-extrabold text-red-500 text-6xl pb-2">404 Not Found</h1>
        <p className="font-bold text-2xl pb-4 text-stone-300"> The page you're looking for does not exist.</p>
        <Link to="/" className='px-5 py-2 bg-red-500 font-bold text-white text-lg rounded-lg'> Go Back </Link>
    </div>
  )
}
export default NotFoundPage