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

    function _sqrt(uint256 y) internal pure returns (uint256 z) {
        if (y > 3) {
            z = y;
            uint256 x = y / 2 + 1;
            while (x < z) {
                z = x;
                x = (y / x + x) / 2;
            }
        } else if (y != 0) {
            z = 1;
        }
        // else z = 0 (default value)
    }

    function _min(uint x, uint y) private pure returns (uint) {
        return x <= y ? x : y;
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

    function addLiquidity(
        uint _amountA,
        uint _amountB
    ) external returns (uint shares) {
        tokenA.transferFrom(msg.sender, address(this), _amountA);
        tokenB.transferFrom(msg.sender, address(this), _amountB);

        // dy * x == dx * y

        if (reserveA > 0 || reserveB > 0) {
            require(
                reserveA * _amountB == reserveB * _amountA,
                "dy * x == dx * y"
            );
        }

        // mint shares
        // s = dx / x * T = dy / y * T
        if (totalSupply == 0) {
            shares = _sqrt(_amountA * _amountB);
        } else {
            shares = _min(
                (_amountA * totalSupply) / reserveA,
                (_amountB * totalSupply) / reserveB
            );
        }

        require(shares > 0, "share is 0");
        _mint(msg.sender, shares);

        // update reserves
        _update(
            tokenA.balanceOf(address(this)),
            tokenB.balanceOf(address(this))
        );
    }

    function removeLiquidity(
        uint _shares
    ) external returns (uint amountA, uint amountB) {
        // calculate amount0 and amount1 to withdraw
        // dx = s / T * x
        // dy = s / T * y
        uint balA = tokenA.balanceOf(address(this));
        uint balB = tokenB.balanceOf(address(this));

        amountA = (_shares * balA) / totalSupply;
        amountB = (_shares * balB) / totalSupply;

        require(amountA > 0 && amountB > 0, "amountA or amountB is 0");

        // burn shares
        _burn(msg.sender, _shares);

        // update reserves
        _update(balA - amountA, balB - amountB);

        // transfer tokens to users
        tokenA.transfer(msg.sender, amountA);
        tokenB.transfer(msg.sender, amountB);
    }

    function getPriceTokenA() public view returns (uint) {
        require(reserveA > 0, "Not enough liquidity");
        return (reserveB * 10 ** 18) / reserveA;
    }

    function getPriceTokenB() public view returns (uint) {
        require(reserveB > 0, "Not enough liquidity");
        return (reserveA * 10 ** 18) / reserveB;
    }
}
