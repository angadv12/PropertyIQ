import { Link } from "react-router-dom";
import PropTypes from 'prop-types';

const ListingCard = ({listing, onDelete}) => {
    const formattedDate = new Date(listing.created_at).toLocaleString("en-US").split(",")[0]

    return (
    <div>
        <div className="relative flex flex-col justify-center border-2 shadow-lg bg-white w-96 px-8 py-4 mr-4 mb-4 rounded-lg">
            <section className="flex flex-col mb-2">
                <div className="flex justify-center">
                    <img
                        className="h-48 rounded-md object-cover mb-4"
                        src={listing.HouseImage || 'https://via.placeholder.com/150'}
                        alt="House"
                    />
                </div>
                <div className="flex items-start">
                    <div className="mr-4 flex flex-col justify-between">
                        <p className="text-lg">Address: {listing.address}</p>
                        <p className="text-lg text-nowrap">City: {listing.city}</p>
                        <p className="text-lg">State: {listing.state}</p>
                    </div>
                    <div className="flex flex-col justify-between">
                        <p className="text-lg text-nowrap">Zipcode {listing.zipcode}</p>
                        <p className="text-lg text-nowrap">Posted: {formattedDate}</p>
                        <p className="text-lg font-semibold">Predicted Price: ${listing.predicted_price ? listing.predicted_price : 'N/A'}</p>
                    </div>
                </div>
            </section>
            <section className="flex items-center -ml-1">
                {onDelete ? (
                    <>
                        <Link
                            to={`/listings/${listing.id}`}
                            className="py-2 px-4 bg-green-400 rounded-md mt-2 hover:bg-green-500 text-white text-sm font-semibold mr-2 w-fit"
                        >
                            View
                        </Link>
                        <button
                            className="py-2 px-4 bg-red-500 rounded-md mt-2 hover:bg-red-600 text-white text-sm font-semibold mr-2"
                            onClick={() => onDelete(listing.id)}
                        >
                            Delete
                        </button>
                    </> ) : (
                    <>
                        <Link
                            to={`/other/listings/${listing.id}`}
                            className="py-2 px-4 bg-green-400 rounded-md mt-2 hover:bg-green-500 text-white text-sm font-semibold mr-2 w-fit"
                        >
                            View
                        </Link>
                        <p className="absolute right-12"> Owner&apos;s ID: {listing.author}</p>
                    </> )
                }
                
            </section>
        </div>
    </div>
    
)}
ListingCard.propTypes = {
    listing: PropTypes.shape({
        created_at: PropTypes.string.isRequired,
        HouseImage: PropTypes.string,
        address: PropTypes.string.isRequired,
        city: PropTypes.string.isRequired,
        state: PropTypes.string.isRequired,
        zipcode: PropTypes.string.isRequired,
        predicted_price: PropTypes.number,
        id: PropTypes.number.isRequired,
        author: PropTypes.string.isRequired,
    }).isRequired,
    onDelete: PropTypes.func,
};

export default ListingCard;