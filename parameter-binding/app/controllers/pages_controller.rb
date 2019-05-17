class PagesController < ApplicationController
    def home
        @user = User.all
      end

      def show
        @user = User.find(params[:id])
      end

      def edit
        @user = User.find(params[:id])
      end
    
      def update
        @user = User.find(params[:id])
        @user.update(user_params)
        redirect_to root_path
      end

      private
      def user_params
        params.require(:user).permit!
      end
end
