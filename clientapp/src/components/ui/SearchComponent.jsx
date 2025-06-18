/* eslint-disable react/prop-types */
import React from "react";
import { X } from "lucide-react";

const SearchComponent = ({
  campaigns,
  searchTerm,
  selectedCampaign,
  onCampaignChange,
  onSearchChange,
  onSearch,
  onClearSearch,
  onKeyPress,
  placeholder = "Search...",
}) => {
  return (
    <div className="w-full flex items-center space-x-4">
      {/* Campaign Selection */}
      <div className="flex items-center space-x-2 flex-shrink-0">
        <label className="text-sm font-medium whitespace-nowrap">
          Campaign
        </label>
        <select
          className="w-48 rounded-md border border-gray-300 p-2"
          value={selectedCampaign?.id || ""}
          onChange={(e) => {
            const campaign = campaigns.find(
              (c) => c.id === parseInt(e.target.value)
            );
            onCampaignChange(campaign);
          }}
        >
          {campaigns.map((campaign) => (
            <option key={campaign.id} value={campaign.id}>
              {campaign.name}
            </option>
          ))}
        </select>
      </div>

      {/* Search Input */}
      <div className="flex flex-1">
        <input
          type="search"
          placeholder={placeholder}
          value={searchTerm}
          onChange={onSearchChange}
          onKeyPress={onKeyPress}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-red-900"
        />
        <button
          onClick={onSearch}
          className="bg-red-900 hover:bg-red-800 text-white px-6 py-2 font-medium transition-colors flex items-center gap-2"
        >
          Search
        </button>
        <button
          onClick={onClearSearch}
          className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-6 py-2 rounded-md font-medium transition-colors flex items-center gap-2"
        >
          <X size={18} />
          Clear
        </button>
      </div>
    </div>
  );
};

export default SearchComponent;
