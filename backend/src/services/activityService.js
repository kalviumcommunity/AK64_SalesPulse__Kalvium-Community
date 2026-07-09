import activityRepository from '../repositories/activityRepository.js';

export class ActivityService {
  async logActivity(activityData) {
    return { message: 'logActivity service placeholder' };
  }

  async getActivities() {
    return { message: 'getActivities service placeholder' };
  }
}

export default new ActivityService();
