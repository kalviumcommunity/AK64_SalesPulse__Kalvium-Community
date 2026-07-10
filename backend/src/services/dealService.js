import dealRepository from '../repositories/dealRepository.js';

export class DealService {
  async createDeal(dealData) {
    return { message: 'createDeal service placeholder' };
  }

  async getDeals() {
    return { message: 'getDeals service placeholder' };
  }
}

export default new DealService();
