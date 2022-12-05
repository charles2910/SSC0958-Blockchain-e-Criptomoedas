//SPDX-License-Identifier: GPL-3.0
// Code based on jocoins ICO https://github.com/hagenderouen/mini-chain/blob/master/hadcoins_ico.sol
// Version of compiler
pragma solidity ^0.8.1;

contract carloscoin_ico {

    // Imprimindo o número máximo de carloscoins à venda
    uint public max_carloscoins = 10000000000;

    // Imprimindo a taxa de conversão de USD para carloscoins (nusp 9805380)
    uint public usd_to_carloscoins = 9805380;

    // Imprimindo o número total de carloscoins que foram comprados por investidores
    uint public total_carloscoins_bought = 0;

    // Mapeamento do endereço do investidor para seu patrimônio em carloscoins para USD
    mapping(address => uint) equity_carloscoins;
    mapping(address => uint) equity_usd;

    // Verificando se um investidor pode comprar carloscoins
    modifier can_buy_carloscoins(uint usd_invested) {
        require (usd_invested * usd_to_carloscoins + total_carloscoins_bought <= max_carloscoins);
        _;
    }

    // Obtendo o patrimônio em carloscoins de um investidor
    function equity_in_carloscoins(address investor) external view returns (uint) {
        return equity_carloscoins[investor];
    }

    // Obtendo o patrimônio em dólares de um investidor
    function equity_in_usd(address investor) external view returns (uint) {
        return equity_usd[investor];
    }

    // Comprando carloscoins
    function buy_carloscoins(address investor, uint usd_invested) external
    can_buy_carloscoins(usd_invested) {
        uint carloscoins_bought = usd_invested * usd_to_carloscoins;
        equity_carloscoins[investor] += carloscoins_bought;
        equity_usd[investor] = equity_carloscoins[investor] / usd_to_carloscoins;
        total_carloscoins_bought += carloscoins_bought;
    }

    // Vendendo carloscoins
    function sell_carloscoins(address investor, uint carloscoins_sold) external
    can_sell_carloscoins(investor, carloscoins_sold) {
        equity_carloscoins[investor] -= carloscoins_sold;
        equity_usd[investor] = equity_carloscoins[investor] / usd_to_carloscoins;
        total_carloscoins_bought -= carloscoins_sold;
    }

    modifier can_sell_carloscoins(address investor, uint carloscoins_sold) {
        require(equity_carloscoins[investor] > carloscoins_sold, "Investor does not have enough coins to sell");
        _;
    }
}
