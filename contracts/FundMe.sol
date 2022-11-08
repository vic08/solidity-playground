// SPDX-License-Identifier: MIT

pragma solidity >=0.6.6 <0.9.0;

// this imports from the npm package
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address[]public funders;

    address public owner;

    constructor(address _priceFeed) public {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function fund() public payable {

        uint256 minimumUSD =  50 * 10 ** 18;
        require(getConversionRate(msg.value) >= minimumUSD, "You need to spend more eth!");

        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);

    }

    function getVersion() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface();
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface();
        (,int256 answer,,,) = priceFeed.latestRoundData();

        return uint256(answer);
    }

    function getConversionRate(uint256 ethAmount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    modifier onlyOwner {
        require(msg.sender == owner, "you can't withdraw");
        _;
    }

    function withdraw() payable onlyOwner public {
        msg.sender.transfer(address(this).balance);
        for (uint256 funderIndex = 0; funderIndex < funders.length; funderIndex++) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;

        }
        funders= new address[](0);
    }
}