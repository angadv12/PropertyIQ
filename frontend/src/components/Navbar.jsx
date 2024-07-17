import { Link, useNavigate, useLocation } from "react-router-dom";
import { useRef, useState, useEffect } from "react";
import { FaUser } from "react-icons/fa";
import logo from "../assets/homelogo.png";

const Navbar = () => {
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const dropdownRef = useRef(null);
    const location = useLocation(); // Get the current location
    const [selectedTab, setSelectedTab] = useState(location.pathname); // Track the selected tab
    const navigate = useNavigate();

    const toggleDropdown = () => {
        setDropdownOpen(!dropdownOpen);
    };

    useEffect(() => {
        setSelectedTab(location.pathname); // Update selected tab when location changes
    }, [location]);

    return (
        <div className="fixed top-0 left-0 right-0 z-50 bg-white border-b-2 border-gray-300">
            <section className="flex flex-col md:flex-row items-center py-2 px-4 md:relative md:py-10">
                <div className="flex items-center justify-center md:absolute md:left-1/2 md:-translate-x-1/2">
                    <Link className="flex items-center" to="/">
                        <img className="size-12" src={logo} alt="Logo" />
                        <h1 className="text-3xl font-bold ml-2"> PropertyIQ </h1>
                    </Link>
                </div>
                <div className="flex items-center mt-2 md:mt-0 md:absolute md:right-2">
                    <Link 
                        to='/' 
                        className={`relative hover:text-blue-400 text-lg font-semibold px-2 py-1 mx-3 flex flex-row justify-center items-center ${selectedTab === '/' ? 'text-blue-500' : ''}`}
                    >
                        Home
                    </Link>
                    <Link 
                        to='/listings' 
                        className={`relative hover:text-blue-400 text-lg font-semibold px-2 py-1 mx-3 flex flex-row justify-center items-center ${selectedTab === '/listings' ? 'text-blue-500' : ''}`}
                    >
                        Your Listings
                    </Link>
                    <Link 
                        to='/profile' 
                        className={`relative hover:text-blue-400 text-lg font-semibold px-2 py-1 mx-3 flex flex-row justify-center items-center ${selectedTab === '/profile' ? 'text-blue-500' : ''}`}
                    >
                        <FaUser className="mr-2"/> Profile
                    </Link>
                </div>
            </section>
        </div>
    );
};
export default Navbar;
