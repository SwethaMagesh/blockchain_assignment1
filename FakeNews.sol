// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract FakeNews {

    struct Checker {
        uint vote;
        uint trustworthiness;
        bool voted;
    }

    struct News {
        uint id;
        bytes32[] content;
        bytes32[] category;
        uint votes;
        uint count;
    }

    mapping(address => uint) public deposit;
    mapping(address => Checker) public checkers;

    News public news;
    uint public PENALTY = 10; 
    // PENALTY IS A FORMULA QUADRATIC TO CONVERGE AT RIGHT TRUSTWORTHINESS

    // CONSTRUCTOR for checker
    constructor() {
        checkers[msg.sender].trustworthiness = 100;
        checkers[msg.sender].voted = false;
    }


    // any valid voter should deposit to become eligible
    function addDeposit() public payable {
        deposit[msg.sender] += msg.value;
    }

    // uplaod a newsitem with content and category
    function uploadNews(uint newsid, bytes32[] memory content, bytes32[] memory category) public {
        news = News(newsid, content, category, 0, 0);
    }


    function vote(uint isreal) public {
        Checker storage sender = checkers[msg.sender];
        // require deposit?
        // require(condition, "Deposit is not enough.");
        require(sender.trustworthiness != 0, "Has no right to vote");
        require(!sender.voted, "Already voted.");
        require(isreal==1 || isreal==0, "Wrong Opinion.");
        sender.voted = true;
        sender.vote = isreal;
        news.votes += isreal*sender.trustworthiness;
        news.count += sender.trustworthiness;
    }

    function getConsensus() public view returns (uint result) {
        result = 0;
        if(news.votes > news.count/2){
            result = 1;
        }
    }

    function updateTrustworthiness(address checker) public {
        if (checkers[checker].vote != getConsensus()) {
            checkers[checker].trustworthiness -= PENALTY;
            deposit[checker] -= 1;
            // penalty for wrong vote from deposit
        } else {
            address payable recv = payable(checker);
            recv.transfer(1);
            // incentive for correct vote
        }
    }

}