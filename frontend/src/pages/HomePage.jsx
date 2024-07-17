import bgImg from "../assets/homePageHouses.jpg";
import { useEffect, useState } from 'react';
import api from '../api';
import ListingCard from "../components/ListingCard";
import { FadeLoader } from "react-spinners";
import { Link } from "react-router-dom";
import { FaArrowRight } from "react-icons/fa6";

const HomePage = () => {
  const [listings, setListings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUserDetails();
    fetchListings();
  }, []);

    const fetchListings = async () => {
      try {
        const response = await api.get('/api/other-users-listings/');
        setListings(response.data);
      } catch (error) {
        console.error('Error fetching listings:', error);
      } finally {
        setIsLoading(false);
      }
    };

    const fetchUserDetails = async () => {
      try {
          const response = await api.get('/api/user/details/');
          setUser(response.data);
      } catch (error) {
          toast.error('Error fetching user details.', {
          position: 'top-center',
          autoClose: 5000,
          });
      }
    };

  return (
    <div className="h-screen relative">
       <div
          className={`relative hero-section w-full ${user ? 'h-96' : 'h-2/3'} bg-cover bg-center`}
          style={{ backgroundImage: `url(${bgImg})`, zIndex: 0 }}
        >
          <h1 className="text-6xl absolute left-20 top-12 text-white font-extrabold text-nowrap"> Find Homes, Get the Value of Your's.</h1>
          {user ? (
            <Link to="/listings" className="absolute left-20 top-3/4 bg-white rounded-lg text-xl py-2 px-4"> Go to Listings </Link>)
            : (<Link className="absolute left-20 top-3/4 bg-white rounded-lg text-xl py-2 px-4"> Get Started </Link>) }
        </div>
        <div className="mx-auto py-8">
          {user ? (<h2 className="text-3xl font-bold mb-8 text-center">Other Users' Listings</h2>) : ('') }
          <div className="flex justify-evenly items-center flex-wrap">
            {user ? (
              isLoading ?
                (<div className="flex items-center justify-center">
                  <FadeLoader color="#000000" />
                </div>) : (
                  listings.map(listing => (
                  <ListingCard listing={listing} key={listing.id}/>)))
            ) : (
              <div className=" flex flex-col items-center">
                <Link to="/login" className="py-3 px-6 bg-blue-500 hover:bg-blue-600 text-white border-2 rounded-lg text-2xl font-bold mb-4">
                  Login
                </Link>
                <Link to="/register" className="py-1 px-2 flex items-center bg-white hover:bg-gray-200 text-gray-500 border-2 rounded-lg text-md font-bold">
                  Don't have an account? Register <FaArrowRight className="mr-2"/>
                </Link>
              </div>
            )}
          </div>
        </div>
    </div>
  )
}
export default HomePage