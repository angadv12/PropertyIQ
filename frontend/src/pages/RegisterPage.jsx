import Form from '../components/Form'
import { Link } from 'react-router-dom'
import { FaArrowRight } from 'react-icons/fa6'

const RegisterPage = () => {
  return (
    <div className='flex flex-col justify-center items-center mt-16'>
        <Form route='/api/user/register/' method='register'/>
        <Link to="/login" className='flex items-center bg-white text-gray-500 shadow-xl rounded-lg px-4 py-2'>Have an account? Sign in <FaArrowRight className='ml-2'/></Link>
    </div>
  )
}
export default RegisterPage