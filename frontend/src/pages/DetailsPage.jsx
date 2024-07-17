import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import api from "../api";
import { toast } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';
import { FadeLoader } from "react-spinners";

const DetailsPage = () => {
    const [listings, setListings] = useState([]); // all user listings
    const [listing, setListing] = useState({}); // listing to view
    const { listingId } = useParams();
    const [formData, setFormData] = useState({});
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchListings = async () => {
            try {
                const fetchedListings = await getListings();
                setListings(fetchedListings);
                if (!fetchedListings.some(listing => listing.id.toString() === listingId)) {
                    toast.error('Listing not found.', { position: 'top-center', autoClose: 5000 });
                    navigate('/');
                } else {
                    getListing();
                }
            } catch (error) {
                console.error("Error fetching listings:", error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchListings();
    }, [listingId, navigate]);

    const getListings = async () => {
        try {
            const res = await api.get('/api/listings/');
            return res.data;
        } catch (err) {
            console.error(err);
        }
    };

    const getListing = async () => {
        try {
            const res = await api.get(`/api/listings/${listingId}/`);
            setListing(res.data);
            console.log(res.data); // log for debugging
        } catch (err) {
            console.error(err);
            toast.error('Error fetching listing.', { position: 'top-center', autoClose: 5000 });
        }
    };

    const areAllRequiredFieldsPresent = () => {
        const requiredFields = ['BedroomAbvGr', 'FullBath', 'HalfBath', 'BldgType', 'GrLivArea', 'GarageCars', 'YearBuilt', 'Utilities', 'ExterQual', 'Foundation', 'CentralAir', 'YrSold'];
        return requiredFields.every(field => listing[field] !== null && listing[field] !== undefined);
    };

    const handlePredictPrice = async () => {
        try {
            console.log("Listing data being sent:", listing); // Log the listing data for debugging
            const res = await api.post(`/api/listings/${listingId}/predict/`, listing);
            setListing({ ...listing, predicted_price: Math.ceil(res.data.predicted_price * 100) / 100.0 });
            toast.success('Price predicted successfully!', { position: 'top-center', autoClose: 5000 });
        } catch (err) {
            console.error("Error predicting price:", err.response ? err.response.data : err.message);
            toast.error('Error predicting price.', { position: 'top-center', autoClose: 5000 });
        }
    }
    
    if(isLoading) {
        return  <div className="h-screen flex items-center justify-center">
            <FadeLoader color="#000000" />
        </div>
    }

    return (
        <main className="ml-6 mt-4 mr-6">
            <h1 className="text-4xl font-bold mb-2 ml-4">Listing Details</h1>
            <div className="flex ml-4 w-fit">
                <div className="mb-2 w-fit pb-2 mr-4 mt-4">
                    {/* LOCATION FIELDS */}
                    <div className="border-b-black border-b-2 w-2/3 mb-2">
                        <p className="font-light text-xl"><span className="font-medium">Address:</span> {listing.address}</p>
                        <p className="font-light text-xl"><span className="font-medium">City:</span> {listing.city}</p>
                        <p className="font-light text-xl"><span className="font-medium">State:</span> {listing.state}</p>
                        <p className="font-light text-xl mb-2"><span className="font-medium">Zipcode:</span> {listing.zipcode}</p>
                    </div>
                        {/* REQUIRED FIELDS */}
                    <div>

                    </div>
                    <p className="font-light text-xl"><span className="font-medium">Bedrooms:</span> {listing.BedroomAbvGr}</p>
                    <p className="font-light text-xl"><span className="font-medium">Full Bath:</span> {listing.FullBath}</p>
                    <p className="font-light text-xl"><span className="font-medium">Half Bath</span> {listing.HalfBath}</p>
                    <p className="font-light text-xl"><span className="font-medium">Type:</span> {listing.choice_fields?.BldgType.display}</p>
                    <p className="font-light text-xl"><span className="font-medium">Living Area (above grade):</span> {listing.GrLivArea} {listing.GrLivArea && 'sq.ft.'}</p>
                    <p className="font-light text-xl"><span className="font-medium">Garage size (cars):</span> {listing.GarageCars}</p>
                    <p className="font-light text-xl"><span className="font-medium">Year Built:</span> {listing.YearBuilt}</p>
                    <p className="font-light text-xl"><span className="font-medium">Utilities:</span> {listing.choice_fields?.Utilities.display}</p>
                    <p className="font-light text-xl"><span className="font-medium">Exterior material quality (1-5):</span> {listing.ExterQual}</p>
                    <p className="font-light text-xl"><span className="font-medium">Foundation:</span> {listing.choice_fields?.Foundation.display}</p>
                    <p className="font-light text-xl"><span className="font-medium">Central A/C?:</span> {listing.CentralAir}</p>
                    <p className="font-light text-xl"><span className="font-medium">Year Sold (most recent):</span> {listing.YrSold}</p>
                </div>
                    {/* OPTIONAL FIELDS */}
                <div className="mb-2 w-fit pb-2 mt-4">
                    <p className="font-light text-xl"><span className="font-medium">Overall material quality (1-10):</span> {listing.OverallQual}</p>
                    <p className="font-light text-xl"><span className="font-medium">Pool Area:</span> {listing.PoolArea} {listing.PoolArea && 'sq.ft.'}</p>
                    <p className="font-light text-xl"><span className="font-medium">Paved Driveway?:</span> {listing.choice_fields?.PavedDrive.display}</p>
                    <p className="font-light text-xl"><span className="font-medium">Garage Area:</span> {listing.GarageArea} {listing.GarageArea && 'sq.ft.'}</p>
                    <p className="font-light text-xl"><span className="font-medium"># Fireplaces:</span> {listing.Fireplaces}</p>
                    <p className="font-light text-xl"><span className="font-medium"># Kitchens:</span> {listing.KitchenAbvGr}</p>
                    <p className="font-light text-xl"><span className="font-medium">Total Property Area:</span> {listing.LotArea} {listing.LotArea && 'sq.ft.'}</p>
                    <p className="font-light text-xl"><span className="font-medium">Heating:</span> {listing.choice_fields?.Heating.display}</p>
                    <p className="font-light text-xl"><span className="font-medium">Total Basement Area:</span> {listing.TotalBsmtSF} {listing.TotalBsmtSF && 'sq.ft.'}</p>
                    <p className="font-light text-xl"><span className="font-medium">Unfinished Basement Area:</span> {listing.BsmtUnfSF} {listing.BsmtUnfSF && 'sq.ft.'}</p>
                    <p className="font-light text-xl"><span className="font-medium">Exterior material:</span> {listing.choice_fields?.Exterior1st.display}</p>
                    <p className="font-light text-xl"><span className="font-medium">Exterior material (if more than 1):</span> {listing.choice_fields?.Exterior2nd.display}</p>
                    <p className="font-light text-xl"><span className="font-medium">Roof Style:</span> {listing.choice_fields?.RoofStyle.display}</p>
                    <p className="font-light text-xl"><span className="font-medium">Year remodeled (last):</span> {listing.YearRemodAdd}</p>
                    <p className="font-light text-xl"><span className="font-medium">Lot configuration:</span> {listing.choice_fields?.LotConfig.display}</p>
                </div>
                <div className="ml-16 mt-4">
                    <img
                        className="h-96 mr-8 rounded-md object-cover mb-4"
                        src={listing.HouseImage || 'https://via.placeholder.com/150'}
                        alt="House"
                    />
                </div>
            </div>
            {/* PREDICTED PRICE */}
            <p className="text-2xl ml-4 mb-4 font-medium">Predicted Price: $ {listing.predicted_price? listing.predicted_price : 'N/A'}</p>
            <div className="mb-4 ml-4">
                <Link
                    to={`/listings/${listingId}/edit`}
                    className="py-3 px-4 bg-blue-500 rounded-md hover:bg-blue-600 text-white text-lg hover:shadow-lg font-semibold mr-2"
                >
                    Edit Details
                </Link>
                {areAllRequiredFieldsPresent() && (
                    <button
                        className="bg-green-500 px-4 py-2 rounded-md hover:bg-green-600 hover:shadow-lg text-white font-semibold text-lg"
                        onClick={handlePredictPrice}
                    >
                        Predict Price
                    </button>
                )}
            </div>
        </main>
    );
};

export default DetailsPage;
