// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract FakeNews {

    struct Checker {
        uint weight;
        bool voted;
        uint vote;
    }

    struct News {
        uint id;
        uint votes;
        uint count;
    }

    mapping (address => uint) public deposit;
    mapping(address => Checker) public checkers;

    News public news;
    uint public N = 15;

    function uploadNews(uint newsid) public {
        news = News(newsid, 0, 0);
    }

    function addDeposit() public payable {
        deposit[msg.sender] += msg.value;
    }

    function giveWeight(address checker) public {
        require(!checkers[checker].voted, "The voter already voted.");
        require(checkers[checker].weight == 0);
        checkers[checker].weight = 100;
    }

    function vote(uint isreal) public {
        Checker storage sender = checkers[msg.sender];
        require(sender.weight != 0, "Has no right to vote");
        require(!sender.voted, "Already voted.");
        require(isreal==1 || isreal==0, "Wrong Opinion.");
        sender.voted = true;
        sender.vote = isreal;
        news.votes += isreal;
        news.count += 1;
    }

    function getConsensus() public view returns (uint result) {
        result = 0;
        if(news.votes > news.count/2){
            result=1;
        }
    }

    function updateWeight(address checker) public {
        if (checkers[checker].vote != getConsensus()) {
            checkers[checker].weight -= 1;
            deposit[checker] -= 1;
        } else {
            address payable recv = payable(checker);
            recv.transfer(1);
        }
    }

}