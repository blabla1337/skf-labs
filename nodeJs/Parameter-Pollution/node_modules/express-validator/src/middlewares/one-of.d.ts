import { ValidationChain } from '../chain';
import { Middleware, Request } from '../base';
import { Result } from '../validation-result';
export declare type OneOfCustomMessageBuilder = (options: {
    req: Request;
}) => any;
export declare function oneOf(chains: (ValidationChain | ValidationChain[])[], message?: OneOfCustomMessageBuilder): Middleware & {
    run: (req: Request) => Promise<Result>;
};
export declare function oneOf(chains: (ValidationChain | ValidationChain[])[], message?: any): Middleware & {
    run: (req: Request) => Promise<Result>;
};
