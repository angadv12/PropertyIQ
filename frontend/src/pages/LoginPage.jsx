import Form from '../components/Form'
import { FaArrowRight } from 'react-icons/fa6'
import { Link } from 'react-router-dom'

const LoginPage = () => {
  return (
    <div className='flex flex-col justify-center items-center mt-16'>
        <Form route='/api/token/' method='login'/>
        <Link to="/register" className='flex items-center bg-white text-gray-500 shadow-xl rounded-lg px-4 py-2'>Create an account <FaArrowRight className='ml-2'/></Link>
    </div>
  )
}
export default LoginPage