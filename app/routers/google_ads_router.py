from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel
import logging

from ..services.google_ads_service import GoogleAdsService

# Setup logger
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/google-ads", tags=["Google Ads"])

# Define models
class ClientAccount(BaseModel):
    accountId: str
    accountName: str
    currencyCode: str
    status: str

class Campaign(BaseModel):
    campaignId: str
    campaignName: str
    status: str
    type: str
    biddingStrategy: str
    budget: float

class CampaignPerformance(BaseModel):
    campaignId: str
    campaignName: str
    status: str
    impressions: int
    clicks: int
    cost: float
    conversions: float
    averageCpc: float

class BidBudgetUpdate(BaseModel):
    customerId: str
    campaignId: str
    newBudget: Optional[float] = None
    newBid: Optional[float] = None

class UpdateResponse(BaseModel):
    success: bool
    message: str
    update_details: Optional[Dict] = None

# Dependency to get GoogleAdsService instance
async def get_ads_service():
    try:
        service = GoogleAdsService()
        return service
    except Exception as e:
        logger.error(f"Failed to initialize Google Ads service: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to initialize Google Ads service")

@router.get("/accounts", response_model=List[ClientAccount])
async def list_accounts(service: GoogleAdsService = Depends(get_ads_service)):
    """
    List all available client accounts
    """
    try:
        return await service.list_client_accounts()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing accounts: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing accounts: {str(e)}")

@router.get("/campaigns/{customer_id}", response_model=List[Campaign])
async def list_campaigns(
    customer_id: str,
    status: Optional[str] = Query(None, description="Filter campaigns by status (ENABLED, PAUSED, REMOVED)"),
    service: GoogleAdsService = Depends(get_ads_service)
):
    """
    List campaigns for a specific customer account
    """
    try:
        return await service.list_campaigns(customer_id, status)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing campaigns: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing campaigns: {str(e)}")

@router.post("/update-bid-budget", response_model=UpdateResponse)
async def update_bid_budget(
    update_data: BidBudgetUpdate,
    service: GoogleAdsService = Depends(get_ads_service)
):
    """
    Update campaign budget and/or bid
    """
    try:
        if not update_data.newBudget and not update_data.newBid:
            raise HTTPException(status_code=400, detail="Either newBudget or newBid must be provided")
            
        result = await service.update_bid_and_budget(
            update_data.customerId,
            update_data.campaignId,
            update_data.newBudget,
            update_data.newBid
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating bid/budget: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating bid/budget: {str(e)}")

@router.get("/performance/{customer_id}", response_model=List[CampaignPerformance])
async def get_campaign_performance(
    customer_id: str,
    campaign_ids: Optional[str] = Query(None, description="Comma-separated list of campaign IDs"),
    date_range: str = Query("LAST_30_DAYS", description="Time period for the report (e.g., LAST_7_DAYS, LAST_30_DAYS)"),
    service: GoogleAdsService = Depends(get_ads_service)
):
    """
    Get performance metrics for campaigns
    """
    try:
        # Parse campaign IDs if provided
        campaign_id_list = None
        if campaign_ids:
            campaign_id_list = [cid.strip() for cid in campaign_ids.split(",")]
            
        return await service.get_campaign_performance(customer_id, campaign_id_list, date_range)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting campaign performance: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting campaign performance: {str(e)}") 