import { useState, useEffect } from 'react';
import api from '../api';
import ListingCard from '../components/ListingCard';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { FadeLoader } from 'react-spinners';

const HomePage = () => {
    const [listings, setListings] = useState([]) // all user listings
    // state for listing details below ADD
    const [address, setAddress] = useState('')
    const [city, setCity] = useState('')
    const [state, setState] = useState('')
    const [zipcode, setZipcode] = useState(null)
    useEffect(() => {
        getListings()
    }, [])

    const getListings = () => {
        api
            .get('/api/listings/')
            .then((res) => res.data)
            .then((data) => {setListings(data); console.log(data)}) //log for debugging
            .catch((error) => { console.log(error); setListings([]) });
    }

    const deleteListing = (id) => {
        api
            .delete(`/api/listings/${id}/delete/`)
            .then((res) => {
                if (res.status === 204) toast.success('Listing deleted.', {position: 'top-center', autoClose: 2000})
                else toast.error('Failed to delete listing.', {position: 'top-center', autoClose: 3000})
                getListings()
            })
            .catch((error) => { console.log(error) })
    }

    const createListing = (e) => {
        e.preventDefault()
        api
            .post('/api/listings/', {address, city, state, zipcode})
            .then((res) => {
                if (res.status === 201) toast.success('Listing created.', {position: 'top-center', autoClose: 2000})
                else toast.error('Failed to create listing.', {position: 'top-center', autoClose: 3000})
                getListings()
            })
            .catch((error) => { console.log(error) })
    }

    if(!listings) {
        return (
            <div className="flex justify-center items-center h-screen">
                <FadeLoader color='#000000'/>
            </div>
        );
    }

  return (
    <div className='flex items-start justify-between'>
        <div>
            <h2 className='font-bold text-3xl ml-8 my-4'>Your Listings</h2>
            <div className='ml-6 flex flex-wrap'>
                {listings.map((listing) =>
                    <ListingCard listing={listing} onDelete={deleteListing} key={listing.id}/>
                )}
            </div>
        </div>
        <div className='mr-8'>
            <h2 className='font-bold text-3xl ml-2 my-4'> Create listing: </h2>
                <form onSubmit={createListing} className='border-2 shadow-lg flex flex-col bg-white py-8 px-8 rounded-lg mb-8 w-fit'>
                    <div className='flex flex-col'>
                        <div className='flex flex-col mr-2'>
                            <label htmlFor="address" className='ml-1'>Address: </label>
                            <input
                                type="text"
                                id='address'
                                name='address'
                                required
                                onChange={(e) => setAddress(e.target.value)}
                                value={address}
                                className='rounded-md border border-gray-300 p-2 mb-2 hover:bg-gray-100 text-black'
                                placeholder='address'
                            />
                        </div>
                        <div className='flex flex-col mr-2'>
                            <label htmlFor="city" className='ml-1'>City: </label>
                            <input
                                type="text"
                                id='city'
                                name='city'
                                required
                                onChange={(e) => setCity(e.target.value)}
                                value={city}
                                className='rounded-md border border-gray-300 p-2 mb-2 hover:bg-gray-100 text-black'
                                placeholder='city'
                            />  
                        </div>
                        <div className='flex flex-col mr-2'>
                            <label htmlFor="state" className='ml-1'>State: </label>
                            <select
                                id='state'
                                name="state"
                                value={state}
                                onChange={(e) => {setState(e.target.value)}}
                                required
                                className='rounded-md border border-solid border-gray-300 p-2 mb-2 hover:bg-gray-100 text-black'
                            >
                                <option value="">Select</option>
                                <option value="AL">AL</option>
                                <option value="AK">AK</option>
                                <option value="AZ">AZ</option>
                                <option value="AR">AR</option>
                                <option value="CA">CA</option>
                                <option value="CO">CO</option>
                                <option value="CT">CT</option>
                                <option value="DE">DE</option>
                                <option value="FL">FL</option>
                                <option value="GA">GA</option>
                                <option value="HI">HI</option>
                                <option value="ID">ID</option>
                                <option value="IL">IL</option>
                                <option value="IN">IN</option>
                                <option value="IA">IA</option>
                                <option value="KS">KS</option>
                                <option value="KY">KY</option>
                                <option value="LA">LA</option>
                                <option value="ME">ME</option>
                                <option value="MD">MD</option>
                                <option value="MA">MA</option>
                                <option value="MI">MI</option>
                                <option value="MN">MN</option>
                                <option value="MS">MS</option>
                                <option value="MO">MO</option>
                                <option value="MT">MT</option>
                                <option value="NE">NE</option>
                                <option value="NV">NV</option>
                                <option value="NH">NH</option>
                                <option value="NJ">NJ</option>
                                <option value="NM">NM</option>
                                <option value="NY">NY</option>
                                <option value="NC">NC</option>
                                <option value="ND">ND</option>
                                <option value="OH">OH</option>
                                <option value="OK">OK</option>
                                <option value="OR">OR</option>
                                <option value="PA">PA</option>
                                <option value="RI">RI</option>
                                <option value="SC">SC</option>
                                <option value="SD">SD</option>
                                <option value="TN">TN</option>
                                <option value="TX">TX</option>
                                <option value="UT">UT</option>
                                <option value="VT">VT</option>
                                <option value="VA">VA</option>
                                <option value="WA">WA</option>
                                <option value="WV">WV</option>
                                <option value="WI">WI</option>
                                <option value="WY">WY</option>
                            </select>
                        </div>
                        <div className='flex flex-col mr-4'>
                            <label htmlFor="zipcode" className='ml-1'>Zipcode: </label>
                            <input
                                type="text"
                                id='zipcode'
                                name='zipcode'
                                required
                                onChange={(e) => setZipcode(e.target.value)}
                                value={zipcode}
                                className='rounded-md border border-gray-300 p-2 mb-2 hover:bg-gray-100 text-black'
                                placeholder='zipcode'
                            />  
                        </div>
                        <input
                            type="submit"
                            value="Submit"
                            className='bg-blue-500 text-white px-4 h-10 rounded-md cursor-pointer hover:bg-blue-600 mt-6'
                        />
                    </div>
                </form>
        </div>
    </div>
  )
}
export default HomePage