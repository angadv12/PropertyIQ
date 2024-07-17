import HouseDetailsForm from '../components/HouseDetailsForm';
import { useParams } from 'react-router-dom';
import { FaPencil } from 'react-icons/fa6';

const EditListingPage = () => {
    const { listingId } = useParams();
  return (
    <div className='ml-12 mt-4'>
        <h1 className='flex items-center font-bold text-4xl mb-2'>Edit Listing <FaPencil className="ml-2"/></h1>
        <HouseDetailsForm listingId={listingId}/>
    </div>
  )
}
export default EditListingPage