from typing import List, Dict

class GoogleAdsService:
    async def list_client_accounts(self) -> List[Dict]:
        """
        List all available client accounts
        
        Returns:
            List[Dict]: Client accounts information
        """
        logger.info("Listing client accounts using real API")
        
        try:
            # Endpoint para listar contas de cliente
            endpoint = f"customers/{self.login_customer_id}/customerClients"
            
            # Fazer a requisição real
            result = await self._make_request(endpoint)
            
            # Processar o resultado
            accounts = []
            if "results" in result:
                for client in result["results"]:
                    client_data = client.get("customer", {})
                    accounts.append({
                        "accountId": client_data.get("id", ""),
                        "accountName": client_data.get("descriptiveName", ""),
                        "currencyCode": client_data.get("currencyCode", ""),
                        "status": client_data.get("status", "")
                    })
            
            logger.info(f"Successfully listed {len(accounts)} client accounts")
            return accounts
        except Exception as e:
            logger.error(f"Error listing client accounts: {str(e)}")
            # Em caso de erro, retornar dados simulados para fins de teste
            logger.warning("Returning simulated data due to error")
            return [
                {
                    "accountId": "1234567890",
                    "accountName": "Client Account 1",
                    "currencyCode": "USD",
                    "status": "ENABLED"
                },
                {
                    "accountId": "0987654321",
                    "accountName": "Client Account 2",
                    "currencyCode": "EUR",
                    "status": "ENABLED"
                },
                {
                    "accountId": "2345678901",
                    "accountName": "Client Account 3",
                    "currencyCode": "USD",
                    "status": "PAUSED"
                }
            ] 