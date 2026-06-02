import { useQuery, queryOptions } from '@tanstack/react-query';
import { z } from 'zod';
import { api } from '@/lib/api-client';

export const userResponseSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
});

export type UserResponse = z.infer<typeof userResponseSchema>;

export const getUser = ({ userId }: { userId: string }): Promise<UserResponse> => {
  return api.get(`/users/${userId}`);
};

export const getUserQueryOptions = (userId: string) => {
  return queryOptions({
    queryKey: ['users', userId],
    queryFn: () => getUser({ userId }),
  });
};

type UseUserOptions = {
  userId: string;
  queryConfig?: any;
};

export const useUser = ({ userId, queryConfig }: UseUserOptions) => {
  return useQuery({
    ...getUserQueryOptions(userId),
    ...queryConfig,
  });
};
