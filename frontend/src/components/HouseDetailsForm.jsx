import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const HouseDetailsForm = ({ listingId }) => {
  const [isLoading, setIsLoading] = useState(!!listingId);
  const [listing, setListing] = useState({});
  const [houseImage, setHouseImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (listingId) {
      fetchListing(listingId);
    } else {
      toast.error('listing fetch error.', { position: 'top-center', autoClose: 5000 })
    }
  }, [])

  const fetchListing = async (id) => {
    try {
      setIsLoading(true);
      const response = await api.get(`/api/listings/${id}/`);
      setListing(response.data);
      if (response.data.HouseImage) {
        setPreview(response.data.HouseImage);
      }
    } catch (error) {
      console.error('Error fetching listing data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e) => {
    setListing(prevData => ({ ...prevData, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    
    for (const key in listing) {
      if(key === 'HouseImage' && houseImage) {
        formData.append(key, houseImage);
      } else {
        if (listing[key] !== null && listing[key] !== undefined) {
          formData.append(key, listing[key]);
        }
      }
    }
    
    try {
      await api.put(`/api/listings/${listingId}/`, formData);
      navigate(`/listings/${listingId}`)
    } catch (error) {
      toast.error('Error submitting form', { position: 'top-center', autoClose: 3000 });
    }
  }

  const handleImageChange = (e) => {
    const file = e.target.files[0]
    setHouseImage(file)
    setPreview(URL.createObjectURL(file))
  }

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!listing || Object.keys(listing).length === 0) {
    return <div>No listing data available</div>;
  }

  return (
      <form onSubmit={handleSubmit}>
        <div className='flex items-start ml-1'>
          {/* REQUIRED FIELDS */}
          <div className='mb-12'>
            <h2 className='font-bold text-2xl -ml-1 mb-4'>Required Details</h2>
            <div className="flex flex-col">
              <img
                className="w-52 h-52 mr-8 rounded-md object-cover mb-4"
                src={preview || listing.HouseImage || 'https://via.placeholder.com/150'}
                alt="House"
              />
              <label className="text-white font-semibold max-w-64 text-lg mb-3 bg-gray-200 rounded-xl px-4 py-4 -ml-1">
                <p className="mb-2">Change Image:</p>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  className="w-full text-xs cursor-pointer file:cursor-pointer text-gray-500 file:mr-4 file:py-1 file:px-2 file:rounded-full file:border-0 file:text-xs file:font-semibold file:bg-violet-50 file:text-green-600 hover:file:bg-green-50"
                />
              </label>
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Address:</label>
              <input type="string" name="address" value={listing.address} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' required />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>City:</label>
              <input type="string" name="city" value={listing.city} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' required />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>State:</label>
              <select
                    name="state"
                    value={listing.state}
                    onChange={handleChange}
                    className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg'
                    required
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
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Zipcode:</label>
              <input type="string" name="zipcode" value={listing.zipcode} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' required />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Above-grade Living Area (sq ft):</label>
              <input type="number" name="GrLivArea" value={listing.GrLivArea} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' required/>
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Utilities:</label>
              <select name="Utilities" value={listing.Utilities} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' required>
                <option value="">Select</option>
                <option value="AllPub">All public utilities</option>
                <option value="NoSewr">Electricity, Gas, and Water</option>
                <option value="NoSeWa">Electricity and Gas/Water Only</option>
                <option value="ELO">Electricity only</option>
              </select>
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Building Type:</label>
              <select name="BldgType" value={listing.BldgType} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' required>
                <option value="">Select</option>
                <option value="1Fam">Single-family</option>
                <option value="2FmCon">Apartment building</option>
                <option value="TwnhsE">Townhouse end unit</option>
                <option value="TwnhsI">Townhouse inside unit</option>
              </select>
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Year Built:</label>
              <input type="number" name="YearBuilt" value={listing.YearBuilt} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' required />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Rate the quality of the material on exterior (1-5):</label>
              <input type="number" name="ExterQual" value={listing.ExterQual} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' required />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Foundation:</label>
              <select name="Foundation" value={listing.Foundation} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' required>
                <option value="">Select</option>
                <option value="BrkTil">Brick & Tile</option>
                <option value="CBlock">Cinder Block</option>
                <option value="PConc">Poured Concrete</option>
                <option value="Slab">Slab</option>
                <option value="Stone">Stone</option>
                <option value="Wood">Wood</option>
              </select>
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Central Air Conditioning?:</label>
              <select name="CentralAir" value={listing.CentralAir} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' required>
                <option value="">Select</option>
                <option value="Y">Yes</option>
                <option value="N">No</option>
              </select>
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Full Bathrooms:</label>
              <input type="number" name="FullBath" value={listing.FullBath} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' required />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Half Bathrooms:</label>
              <input type="number" name="HalfBath" value={listing.HalfBath} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' required />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Bedrooms (above grade):</label>
              <input type="number" name="BedroomAbvGr" value={listing.BedroomAbvGr} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' required />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Garage Size (in cars):</label>
              <input type="number" name="GarageCars" value={listing.GarageCars} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' required />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Year Last Sold:</label>
              <input type="number" name="YrSold" value={listing.YrSold} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' required />
            </div>
          </div>

          {/* OPTIONAL FIELDS */}
          <div className='ml-4'>
            <h2 className='font-bold text-2xl mb-4 mt-1'>Optional Details</h2>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Pool Area (sq ft):</label>
              <input type="number" name="PoolArea" value={listing.PoolArea} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Paved Driveway:</label>
              <select name="PavedDrive" value={listing.PavedDrive} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' >
                <option value="">Select</option>
                <option value="Y">Paved</option>
                <option value="P">Partial Pavement</option>
                <option value="N">Dirt/Gravel</option>
              </select>
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Garage Area:</label>
              <input type="number" name="GarageArea" value={listing.GarageArea} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Number of Fireplaces:</label>
              <input type="number" name="Fireplaces" value={listing.Fireplaces} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Number of kitchens (above grade):</label>
              <input type="number" name="KitchenAbvGr" value={listing.KitchenAbvGr} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Total Property Area (sq ft):</label>
              <input type="number" name="LotArea" value={listing.LotArea} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Heating:</label>
              <select name="Heating" value={listing.Heating} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' >
                <option value="">Select</option>
                <option value="Floor">Floor Furnace</option>
                <option value="GasA">Gas forced warm air furnace</option>
                <option value="GasW">Gas hot water or steam heat</option>
                <option value="Grav">Gravity furnace</option>
                <option value="OthW">Hot water or steam heat other than gas</option>
                <option value="Wall">Wall furnace</option>
              </select>
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Total Basement Area (sq ft):</label>
              <input type="number" name="TotalBsmtSF" value={listing.TotalBsmtSF} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Unfinished Basement Area (sq ft):</label>
              <input type="number" name="BsmtUnfSF" value={listing.BsmtUnfSF} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Exterior Material:</label>
              <select name="Exterior1st" value={listing.Exterior1st} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' >
                <option value="">Select</option>
                <option value="VinylSd">Vinyl Siding</option>
                <option value="MetalSd">Metal Siding</option>
                <option value="Wd Sdng">Wood Siding</option>
                <option value="HdBoard">Hardboard</option>
                <option value="BrkFace">Brick Face</option>
                <option value="WdShing">Wood Shingles</option>
                <option value="CemntBd">Cement Board</option>
                <option value="Plywood">Plywood</option>
                <option value="AsbShng">Asbestos Shingles</option>
                <option value="Stucco">Stucco</option>
                <option value="BrkComm">Brick Common</option>
                <option value="AsphShn">Asphalt Shingles</option>
                <option value="Stone">Stone</option>
                <option value="ImStucc">Imitation Stucco</option>
                <option value="CBlock">Cinder Block</option>
                <option value="Other">Other</option>
                <option value="PreCast">PreCast</option>
              </select>
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Exterior Material (if more than one):</label>
              <select name="Exterior2nd" value={listing.Exterior2nd} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' >
                <option value="">Select</option>
                <option value="VinylSd">Vinyl Siding</option>
                <option value="MetalSd">Metal Siding</option>
                <option value="Wd Sdng">Wood Siding</option>
                <option value="HdBoard">Hardboard</option>
                <option value="BrkFace">Brick Face</option>
                <option value="WdShing">Wood Shingles</option>
                <option value="CemntBd">Cement Board</option>
                <option value="Plywood">Plywood</option>
                <option value="AsbShng">Asbestos Shingles</option>
                <option value="Stucco">Stucco</option>
                <option value="BrkComm">Brick Common</option>
                <option value="AsphShn">Asphalt Shingles</option>
                <option value="Stone">Stone</option>
                <option value="ImStucc">Imitation Stucco</option>
                <option value="CBlock">Cinder Block</option>
                <option value="Other">Other</option>
                <option value="PreCast">PreCast</option>
              </select>
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Roof Style:</label>
              <select name="RoofStyle" value={listing.RoofStyle} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' >
                <option value="">Select</option>
                <option value="Gable">Gable</option>
                <option value="Hip">Hip</option>
                <option value="Flat">Flat</option>
                <option value="Gambrel">Gambrel (Barn)</option>
                <option value="Mansard">Mansard</option>
                <option value="Shed">Shed</option>
              </select>
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Year Last Remodeled:</label>
              <input type="number" name="YearRemodAdd" value={listing.YearRemodAdd} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Overall Quality (1-10):</label>
              <input type="number" name="OverallQual" value={listing.OverallQual} onWheel={(e) => e.target.blur()} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' />
            </div>
            <div className='flex flex-col w-2/3 mb-2'>
              <label>Lot Configuration:</label>
              <select name="LotConfig" value={listing.LotConfig} onChange={handleChange} className='-ml-1 bg-gray-200 py-2 px-4 rounded-lg' >
                <option value="">Select</option>
                <option value="Inside">Inside lot</option>
                <option value="Corner">Corner lot</option>
                <option value="CulDSac">Cul-de-Sac</option>
                <option value="FR2">Frontage on 2 sides</option>
              </select>
            </div>
            <button type="submit" className='ml-8 mb-4 mt-4 px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg text-white font-semibold'>
              Update Listing
            </button>
          </div>
        </div>
        
      </form>
  );
};

export default HouseDetailsForm;