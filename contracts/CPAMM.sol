// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.30;
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract CPAMM {
    ERC20 public immutable tokenA;
    ERC20 public immutable tokenB;

    uint public reserveA;
    uint public reserveB;

    uint public totalSupply;
    mapping(address => uint) public balanceOf;

    constructor(address _tokenA, address _tokenB) {
        tokenA = ERC20(_tokenA);
        tokenB = ERC20(_tokenB);
        testNumber = 20;
    }

    function _mint(address _to, uint _amount) private {
        balanceOf[_to] += _amount;
        totalSupply += _amount;
    }

    function _burn(address _from, uint _amount) private {
        balanceOf[_from] -= _amount;
        totalSupply -= _amount;
    }

    function _update(uint _reserveA, uint _reserveB) private {
        reserveA = _reserveA;
        reserveB = _reserveB;
    }

    function swap(
        address _tokenIn,
        uint _amountIn
    ) external returns (uint amountOut) {
        require(
            _tokenIn == address(tokenA) || _tokenIn == address(tokenB),
            "Invalid token"
        );
        require(_amountIn > 0, "amount in = 0");

        // pull in token in
        bool isTokenA = _tokenIn == address(tokenA);
        (
            ERC20 tokenIn,
            ERC20 tokenOut,
            uint reserveIn,
            uint reserveOut
        ) = isTokenA
                ? (tokenA, tokenB, reserveA, reserveB)
                : (tokenB, tokenA, reserveB, reserveA);

        tokenIn.transferFrom(msg.sender, address(this), _amountIn);

        // calculate token out: dy = y*dx / (x + dx)
        amountOut = (reserveOut * _amountIn) / (reserveIn + _amountIn);

        // transfer token out to msg.sender
        tokenOut.transfer(msg.sender, amountOut);

        // update the reserves
        _update(
            tokenA.balanceOf(address(this)),
            tokenB.balanceOf(address(this))
        );
    }

    function addLiquidity() external {}

    function removeLiquidity() external {}
}
